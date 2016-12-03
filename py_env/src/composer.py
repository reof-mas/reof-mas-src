from creamas import CreativeAgent, Artifact

class ComposerAgent(CreativeAgent):
    '''
    Agent generates new melodies based on a markov chain.
    '''
    def __init__(self, env, transition_probs):
        '''

        :param env:
            subclass of :py:class:`~creamas.core.environment.Environment`
        :param transition_probs:
            markov chain containing transition probabilities
        '''
        super().__init__(env)
        self.transition_probs = transition_probs

    def generate(self, max_len = 10):
        '''
        Generates a random sentence using markov chain probabilities.

        :param
            max_len: maximum length of the generated melody
        :return:
            Artifact containing generated sentence
        '''
        import random

        # Choose start note randomly
        start = random.choice(list(self.transition_probs))
        next_states = list(self.transition_probs[start].items())

        # melody is a list of the selected notes
        melody = [start]
        curr_len = 1

        # Generate the melody
        while curr_len < max_len:
            # Choose next state
            sum = 0
            rnd = random.random()

            for i in range(len(next_states)):
                # State is chosen if rnd < cumulative sum of transition probabilities
                if rnd <= sum + next_states[i][1]:
                    melody.append(next_states[i][0])
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



