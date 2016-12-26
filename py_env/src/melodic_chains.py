"""
This is the entry point of our program.
"""

from music_environment import MusicEnvironment
import markov_chain
import math
from composer import ComposerAgent
from audience_agent import AudienceAgent
from creamas import Simulation
from serializers import get_artifact_ser
from utility import *
from music21 import *
import aiomas
import copy


def _init_agents(env, agent_number, folder1, folder2, ordr, audience):
    """
    Creates composer agents.

    Args:
        env: environment for the agents
        agent_number: amount of agents to create
        folder1: directory path of an inspiring set
        folder2: directory path of another insipiring set
        ordr: order of the markov chains
        audience: audience agent
    """
    agent_vocab = 0
    tc1 = markov_chain.get_markov_chain(folder1, order=ordr)
    tc2 = markov_chain.get_markov_chain(folder2, order=ordr)
    for i in range(agent_number):
        if agent_vocab < math.ceil(agent_number/2):
            agent = ComposerAgent(env, tc1, audience.addr)
        else:
            agent = ComposerAgent(env, tc2, audience.addr)
        agent_vocab += 1


def main():
    """
    The main function of the program.
    """
    # Delete all the contents, midi files, in the outputs folder
    delete_outputs('outputs')
    instrument_list = get_instruments()

    # Number of iterations in the simulation
    iteration = 5
    # Number of agents to create
    agent_number = 6
    # Order of the markov chains
    selected_order = 2
    # Inspiring set paths
    path1 = "../../melodies/classical/schubert"
    path2 = "../../melodies/classical/bach"
    #directory_path = "../../melodies/classical/schubert"
    #transition_counts = markov_chain.get_markov_chain(directory_path, order=selected_order)

    env = MusicEnvironment.create(('localhost', 5555), codec=aiomas.MsgPack, extra_serializers=[get_artifact_ser])
    env.log_folder = 'logs'

    # Create audience
    audience = AudienceAgent(env)

    _init_agents(env, agent_number, path1, path2, selected_order, audience)

    sim = Simulation(env, log_folder='logs', callback=env.vote)
    sim.async_steps(iteration)
    sim.end()

    # Test this
    MusicEnvironment.shutdown(env)

    #create_song2(env.artifacts)
    create_song(env.artifacts)


def create_song(domain_artifacts):
    """
    Creates a song from domain artifacts. Creates a two track song with random thematic transformations. Selects the most complex and the least complex theme for different tracks.

    Args:
        domain_artifacts: list of domain artifacts
    """
    # Choose the artifacts with lowest and highest complexities for different tracks in the song
    highest_complexity = 1
    lowest_complexity = 0
    most_complex = domain_artifacts[0]
    least_complex = domain_artifacts[0]

    for artifact in domain_artifacts:
        similarity = self_similarity(artifact)
        if similarity < highest_complexity:
            highest_complexity = similarity
            most_complex = artifact
        if similarity > lowest_complexity:
            lowest_complexity = similarity
            least_complex = artifact

    part1 = sequence_to_part(least_complex.obj)
    motif2 = sequence_to_part(most_complex.obj)
    part2 = stream.Part()

    # Change octave of the simpler part
    for note in part1:
        note.octave = 3

    # Pick random thematic transformations
    for i in range(5):
            number1 = random.randint(0, 3)
            if number1 is 0:
                #seq1 = transpose(motif1, random.randint(0, 11))
                seq2 = transpose(motif2, random.randint(0, 11))
            elif number1 is 1:
                #seq1 = inverse(motif1)
                seq2 = inverse(motif2)
            elif number1 is 2:
                #seq1 = retrograde(motif1)
                seq2 = retrograde(motif2)
            elif number1 is 3:
                #seq1 = inverse_and_retrograde(motif1)
                seq2 = inverse_and_retrograde(motif2)

            #for note in seq1:
                #part1.append(copy.copy(note))

            for note in seq2:
                part2.append(copy.copy(note))

    # Make part2 as long as part1
    # part2_len = len(part2)
    # while part2.duration.quarterLength < part1.duration.quarterLength:
    #     for i in range(part2_len):
    #         part2.append(copy.copy(part2[i]))

    # Make part1 as long as part2
    part1_len = len(part1)
    while part1.duration.quarterLength < part2.duration.quarterLength:
        for i in range(part1_len):
            part1.append(copy.copy(part1[i]))

    # Write the song to file
    change_instrument(part1, random.randint(0, 127))
    change_instrument(part2, random.randint(0, 127))
    song = stream.Stream([part1, part2])
    song.write('midi', 'outputs/the_song.mid')


def create_song2(domain_artifacts):
    """
    Creates a song from domain artifacts. Creates a monophonic song with random thematic transformations.

    Args:
        domain_artifacts: list of domain artifacts
    """
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

    motif1 = sequence_to_stream(most_complex.obj)
    #motif2 = sequence_to_stream(most_complex.obj)

    # Change octave of the simpler part
    for note in motif1:
        note.octave = 3

    # Pick random thematic transformations
    final_stream=stream.Stream()
    final_stream.append(motif1)
    for i in range(5):
        number1=random.randint(0,3)
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
    song.write('midi', 'outputs/the_song.mid')

def create_songs(domain_artifacts):
    """
    Creates a song from all the themes in domain artifacts.

    Args:
        domain_artifacts: list of domain artifacts
    """
    j = 1
    for artifact in domain_artifacts:
        motif1 = sequence_to_stream(artifact.obj)
        final_stream=stream.Stream()
        final_stream.append(motif1)
        for i in range(5):
            number1=random.randint(0,3)
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
        song.write('midi', 'outputs/the_song' + str(j) + '.mid')
        j += 1



def create_song3(domain_artifacts):
    """
    Creates a song from domain artifacts. Creates a two track song with random thematic transformations. Selects the most complex and the least complex theme for different tracks.

    Args:
        domain_artifacts: list of domain artifacts
    """
    # Choose the artifacts with lowest and highest complexities for different tracks in the song
    highest_complexity = 1
    lowest_complexity = 0
    most_complex = domain_artifacts[0]
    least_complex = domain_artifacts[0]

    for artifact in domain_artifacts:
        similarity = self_similarity(artifact)
        if similarity < highest_complexity:
            highest_complexity = similarity
            most_complex = artifact
        if similarity > lowest_complexity:
            lowest_complexity = similarity
            least_complex = artifact

    part1 = sequence_to_part(least_complex.obj)
    motif2 = sequence_to_part(most_complex.obj)
    part2 = stream.Part()
    tonality = key.Key("C")
    base_tonality = tonality
    current.tonality = tonality
    modality_changer=0
    while tonality is not base_tonality & modality_changer<5:
        while current.tonality == tonality:
            number1 = random.randint(0, 3)

            if number1 is 0:
                # seq1 = transpose(motif1, random.randint(0, 11))
                seq2 = diatonic_transposition(motif2, random.randint(0, 11), current.tonality)
            elif number1 is 1:
                # seq1 = inverse(motif1)
                seq2 = inverse(motif2)
            elif number1 is 2:
                # seq1 = retrograde(motif1)
                seq2 = retrograde(motif2)
            elif number1 is 3:
                # seq1 = inverse_and_retrograde(motif1)
                seq2 = inverse_and_retrograde(motif2)

    # Change octave of the simpler part
        for note in part1:
            note.octave = 3

    # Pick random thematic transformations
    for i in range(5):
            number1 = random.randint(0, 3)
            if number1 is 0:
                #seq1 = transpose(motif1, random.randint(0, 11))
                seq2 = transpose(motif2, random.randint(0, 11))
            elif number1 is 1:
                #seq1 = inverse(motif1)
                seq2 = inverse(motif2)
            elif number1 is 2:
                #seq1 = retrograde(motif1)
                seq2 = retrograde(motif2)
            elif number1 is 3:
                #seq1 = inverse_and_retrograde(motif1)
                seq2 = inverse_and_retrograde(motif2)

            #for note in seq1:
                #part1.append(copy.copy(note))

            for note in seq2:
                part2.append(copy.copy(note))

    # Make part2 as long as part1
    # part2_len = len(part2)
    # while part2.duration.quarterLength < part1.duration.quarterLength:
    #     for i in range(part2_len):
    #         part2.append(copy.copy(part2[i]))

    # Make part1 as long as part2
    part1_len = len(part1)
    while part1.duration.quarterLength < part2.duration.quarterLength:
        for i in range(part1_len):
            part1.append(copy.copy(part1[i]))

    # Write the song to file
    change_instrument(part1, random.randint(0, 127))
    change_instrument(part2, random.randint(0, 127))
    song = stream.Stream([part1, part2])
    song.write('midi', 'outputs/the_song.mid')

if __name__ == "__main__":
    main()
