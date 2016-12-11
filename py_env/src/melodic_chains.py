from music_environment import MusicEnvironment
import markov_chain
from composer import ComposerAgent
from creamas import Simulation
from utility import *
from music21 import *
import copy

def main():
    # Delete all the contents, midi files, in the outputs folder
    delete_outputs('outputs')
    instrument_list = get_instruments()

    selected_order = 2
    directory_path = "../../melodies/classical/bach"
    transition_counts = markov_chain.get_markov_chain(directory_path, order=selected_order)

    env = MusicEnvironment.create(('localhost', 5555))
    env.log_folder = 'logs'
    for i in range(5):
        agent = ComposerAgent(env, transition_counts)

    # Audience agents also?

    sim = Simulation(env, log_folder='logs', callback=env.vote)
    sim.async_steps(5)
    sim.end()
    # Test this
    MusicEnvironment.shutdown(env)

    # Concatenate the melodies
    #concat_melodies(env.artifacts, instrument_list)
    create_song(env.artifacts)


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

def create_song(domain_artifacts):
    # Choose the artifacts with lowest and highest complexities for different tracks in the song
    highest_complexity = 0
    lowest_complexity = 1
    most_complex = domain_artifacts[0]
    least_complex = domain_artifacts[0]

    for artifact in domain_artifacts:
        similarity = self_similarity(artifact)
        if similarity > highest_complexity:
            highest_complexity = similarity
            most_complex = artifact
        if similarity < lowest_complexity:
            lowest_complexity = similarity
            least_complex = artifact

    part1 = sequence_to_part(least_complex.obj)
    part2 = sequence_to_part(most_complex.obj)

    # Change octave of the simpler part
    for note in part1:
        note.octave = 3

    # Duplicate part1 a couple of times
    for i in range(2):
        for note in part1:
            part1.append(copy.copy(note))

    # Make part2 as long as part1
    part2_len = len(part2)
    while part2.duration.components[0][2] < part1.duration.components[0][2]:
        for i in range(part2_len):
            part2.append(copy.copy(part2[i]))

    # Write the song to file
    change_instrument(part1, random.randint(0, 127))
    change_instrument(part2, random.randint(0, 127))
    song = stream.Stream([part1, part2])
    song.write('midi', 'outputs/the_song.midi')

if __name__ == "__main__":
    main()
