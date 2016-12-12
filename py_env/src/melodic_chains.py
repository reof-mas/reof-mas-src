from music_environment import MusicEnvironment
import markov_chain
from composer import ComposerAgent
from audience_agent import AudienceAgent
from creamas import Simulation
from serializers import get_artifact_ser
from utility import *
from music21 import *
import aiomas
import copy

def main():
    # Delete all the contents, midi files, in the outputs folder
    delete_outputs('outputs')
    instrument_list = get_instruments()

    selected_order = 2
    #directory_path = "../../melodies/classical/bach"
    #directory_path = "../../melodies/classical/mozart"
    directory_path = "../../melodies/classical/schubert"
    transition_counts = markov_chain.get_markov_chain(directory_path, order=selected_order)

    env = MusicEnvironment.create(('localhost', 5555), codec=aiomas.MsgPack, extra_serializers=[get_artifact_ser])
    env.log_folder = 'logs'

    # Create audience
    audience = AudienceAgent(env)

    for i in range(5):
        agent = ComposerAgent(env, transition_counts, audience.addr)

    sim = Simulation(env, log_folder='logs', callback=env.vote)
    sim.async_steps(5)
    sim.end()
    # Test this
    MusicEnvironment.shutdown(env)

    # Concatenate the melodies
    #concat_melodies(env.artifacts, instrument_list)
    create_song2(env.artifacts)


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


def create_song2(domain_artifacts):
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

    motif1 = sequence_to_stream(least_complex.obj)
    motif2 = sequence_to_stream(most_complex.obj)

    # Change octave of the simpler part
    for note in motif1:
        note.octave = 3

    #
    final_stream=stream.Stream()
    final_stream.append(motif1)
    for i in range(5):
        number1=random.randint(0,4)
        if number1 is 0:
            final_stream.append(transpose(motif1, random.randint(0,11)))
        elif number1 is 1:
            final_stream.append(inverse(motif1))
        elif number1 is 2:
            final_stream.append(retrograde(motif1))
        elif number1 is 3:
            final_stream.append(inverse_and_retrograde(motif1))
    final_stream.append(inverse(motif1))

    # Write the song to file
    change_instrument(final_stream, random.randint(0, 127))
    song = stream.Stream(final_stream)
    song.write('midi', 'outputs/the_song.midi')

if __name__ == "__main__":
    main()
