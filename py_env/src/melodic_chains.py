from music_environment import MusicEnvironment
import markov_chain
from composer import ComposerAgent
from creamas import Simulation


def main():
    selected_order = 1
    directory_path = "../../melodies/classical/bach"
    transition_probs = markov_chain.get_markov_chain(directory_path, order=selected_order)

    env = MusicEnvironment.create(('localhost', 5555))
    env.log_folder = 'logs'
    for i in range(10):
        agent = ComposerAgent(env, transition_probs)

    # Audience agents also?

    sim = Simulation(env, log_folder='logs', callback=env.vote)
    sim.async_steps(2)
    sim.end()

    # Test this
    MusicEnvironment.shutdown(env)

if __name__ == "__main__":
    main()
