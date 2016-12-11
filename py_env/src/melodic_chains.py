from music_environment import MusicEnvironment
import markov_chain
from composer import ComposerAgent
from creamas import Simulation
from utility import *
from music21 import *
import random


def main():
    # Delete all the contents, midi files, in the outputs folder
    delete_outputs('outputs')
    instrument_list = get_instruments()

    selected_order = 2
    directory_path = "../../melodies/classical/bach"
    transition_counts = markov_chain.get_markov_chain(directory_path, order=selected_order)

    env = MusicEnvironment.create(('localhost', 5555))
    env.log_folder = 'logs'
    for i in range(10):
        agent = ComposerAgent(env, transition_counts)

    # Audience agents also?

    sim = Simulation(env, log_folder='logs', callback=env.vote)
    sim.async_steps(10)
    sim.end()
    # Test this
    MusicEnvironment.shutdown(env)

    # Concatenate the melodies
    concat_melodies(env.artifacts, instrument_list)


# TODO: change the argument types
# Find a way to combine the melodies not just concat them
def concat_melodies(a, instrument_list):
    s = stream.Stream()
    for i in range(len(a)):
        t = sequence_to_stream(a[i].obj)
        instrument_program = instrument_family(instrument_list, 'percussive')
        # change_instrument(t, random.randint(0, 127))
        change_instrument(t, instrument_program)
        s.append(t)

    s.write('midi', 'outputs/song.mid')


if __name__ == "__main__":
    main()
