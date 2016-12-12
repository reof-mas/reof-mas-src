from creamas import CreativeAgent, Artifact
from list_memory import ListMemory
import utility
import logging
import markov_chain
import random
import aiomas


class ComposerAgent(CreativeAgent):
    """
    Agent generates new melodies based on a markov chain.
        Args:
        env: subclass of :py:class:`~creamas.core.environment.Environment`
        transition_counts: transition counts of a markov chain
        audience_addr: address of the audience agent
        order: the order of the markov chain
        log_folder: folder for logs
    """
    def __init__(self, env, transition_counts, audience_addr, order=1, log_folder = 'logs'):
        super().__init__(env, log_folder=log_folder)
        self.transition_counts = transition_counts
        self.transition_probs = {}
        self.order = order
        self.mem = ListMemory(20)
        self.N = 10 # invent length
        self.audience_addr = audience_addr

        # Calculate transition probabilities
        self.update_stp()

    def update_stp(self):
        """
        Converts state transition counts to probabilities
        """
        for state, succ_counts in self.transition_counts.items():
            #print("state: {}, succ_counts: {}".format(state, succ_counts))
            self.transition_probs[state] = markov_chain.get_transitions_probs_for_state(succ_counts)

    def generate(self, max_len = 10):
        """
        Generates a random sentence using markov chain probabilities.

        Args:
            max_len: maximum length of the generated melody
        Returns:
            Artifact containing generated melody
        """

        # Choose start note randomly
        start = random.choice(list(self.transition_probs))
        next_states = list(self.transition_probs[start].items())

        # melody is a list of the selected notes
        melody = []
        for note in start:
            melody.append(note)
        curr_len = 1

        # Generate the melody
        while curr_len < max_len:
            # Choose next state
            sum = 0
            rnd = random.random()

            for i in range(len(next_states)):
                # State is chosen if rnd < cumulative sum of transition probabilities
                if rnd <= sum + next_states[i][1]:
                    melody.append(next_states[i][0][self.order-1])
                    curr_len += 1

                    # If selected state doesn't have transitions, return melody
                    if next_states[i][0] not in self.transition_probs:
                        return Artifact(self, melody)

                    # Get the possible transitions from selected state
                    next_states = list(self.transition_probs[next_states[i][0]].items())
                    break
                else:
                    sum += next_states[i][1]

        return Artifact(self, melody)

    def value(self, artifact):
        """
        Computes value of an artifact. Currently only uses Zipf's law.

        Args:
            artifact: artifact to be evaluated
        Returns:
            Value of the artifact
        """

        return utility.zipfs_law(artifact)

    async def invent(self, n):
        """
        Invents a new melody. Generates n melodies and selects the best.

        Args:
            n: The number of melodies generated.
        Returns:
            A melody wrapped as :class:`~creamas.core.artifact.Artifact` and its
            evaluation.
        """
        best_artifact = self.generate()
        max_evaluation, framing = self.evaluate(best_artifact)
        audience = await self.env.connect(self.audience_addr)
        for _ in range(n-1):
            artifact = self.generate()
            self_evaluation, fr = self.evaluate(artifact)
            audience_opinion = await audience.give_opinion(artifact)
            evaluation  = (self_evaluation + audience_opinion) / 2
            if evaluation > max_evaluation:
                best_artifact = artifact
                max_evaluation = evaluation
                framing = fr

        self.logger.log(logging.DEBUG, "{} invented word: {} (eval={}, framing={})"
                     .format(self.name, best_artifact.obj, max_evaluation,
                             framing))

        # Add evaluation and framing to the artifact
        best_artifact.add_eval(self, max_evaluation, fr=framing)

        # Memorize best_artifact
        self.mem.memorize(best_artifact)

        return best_artifact


    def learn(self, artifact):
        """
        Adds transitions in artifact to state transition counts and updates state transition probabilities.

        Args:
            artifact: Artifact to be learnt
        """
        # Get text inside of the artifact object
        states = markov_chain.get_states(artifact.obj, self.order)
        #print("Incoming artefact {}".format(notes))

        markov_chain.add_transitions(states, self.transition_counts)
        # Dont forget to update state transition probabilities
        for i in range(len(states)-1):
            self.transition_probs[states[i]] = markov_chain.get_transitions_probs_for_state(self.transition_counts[states[i]])

    def evaluate(self, artifact):
        """
        Evaluates an artifact based on value, novelty and surprise.

        Args:
            artifact: artifact to be evaluated
        Returns:
            evaluation and framing
        """
        value = self.value(artifact)
        novelty, novelty_framing = self.novelty(artifact)
        surprise = self.surprise(artifact)
        # Change value framing if we can
        framing = {'value': artifact.obj, 'novelty': novelty_framing}
        evaluation = (value + novelty + surprise) / 3
        return evaluation, framing

    def novelty(self, artifact):
        """
        Calculates novelty of an artifact based on Levenshtein distance.

        Args:
            artifact: Artifact containing melody.
        Returns:
            Novelty of the artifact
        """

        # Return 1 if no artifacts in memory
        if len(self.mem.artifacts) == 0:
            return 1.0, None

        novelty = 1.0
        evaluation_melody = artifact.obj
        matching_melody = self.mem.artifacts[0].obj
        steps = utility.convert_melody_to_steps(evaluation_melody)

        for memart in self.mem.artifacts:
            melody = memart.obj
            lev = utility.levenshtein(steps, utility.convert_melody_to_steps(melody))
            mlen = max(len(evaluation_melody), float(len(melody)))
            current_novelty = float(lev) / mlen
            if current_novelty < novelty:
                novelty = current_novelty
                matching_melody = melody

        return novelty, matching_melody

    def surprise(self, artifact):
        """
        Calculates the surprisingness of an artifact based on the pseudo-likelihood of it being created using the agent's Markov chain.

        Args:
            artifact: artifact to be evaluated
        Returns:
            Surprisingness of an artifact
        """
        likelihood = 1
        states = markov_chain.get_states(artifact.obj, self.order)

        for i in range(len(states)-1):
            if states[i] not in self.transition_probs or states[i+1] not in self.transition_probs[states[i]]:
                likelihood *= 0.1
            else:
                likelihood *= self.transition_probs[states[i]][states[i+1]]

        return 1-likelihood

    async def act(self):
        """
        Agent memorizes and learns a random artifact from domain. Then agent invents a new artifact, which is then memorized and added to candidates for voting.
        """
        # Add random domain artifacts to memory
        if len(self.env.artifacts) > 0:
            domain_artifact = random.choice(self.env.artifacts)
            self.mem.memorize(domain_artifact)
            # Add the artifact into the state transition counts,
            self.learn(domain_artifact)


        # Invent a new melody
        artifact = await self.invent(self.N)
        # Add the artifact itself to memory
        self.mem.memorize(artifact)

        self.logger.log(logging.DEBUG, [a.obj for a in self.mem.artifacts])
        self.env.add_candidate(artifact)


