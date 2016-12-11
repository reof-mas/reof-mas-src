import os, shutil
from music21 import *
from numpy import genfromtxt
import random

def levenshtein(s, t):
    """Compute the edit distance between two strings.
    From Wikipedia article; Iterative with two matrix rows.
    """
    if s == t:
        return 0
    elif len(s) == 0:
        return len(t)
    elif len(t) == 0:
        return len(s)
    v0 = [None] * (len(t) + 1)
    v1 = [None] * (len(t) + 1)
    for i in range(len(v0)):
        v0[i] = i
    for i in range(len(s)):
        v1[0] = i + 1
        for j in range(len(t)):
            cost = 0 if s[i] == t[j] else 1
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
        for j in range(len(v0)):
            v0[j] = v1[j]

    return v1[len(t)]


def convert_melody_to_steps(melody):


    steps = []
    for i in range(len(melody) - 1):
        note1 = melody[i]
        note2 = melody[i + 1]
        steps.append(interval.notesToChromatic(note.Note(note1[0]), note.Note(note2[0])).intervalClass)

    return steps


# Self similarity : an example usage
# I = ['A','B','B','B','C','A','B']
# I2 = ['A','B','C','B','A','C']
# I3 = ['A','B','C','D','E']
# I4 = ['A','B','C','D','E','F','G','T','N']
# I5 = ['E','E','E','E','E']
# self_similarity(I)
def self_similarity(artifact):
    """

    :param I:
    :return:
    """

    melody = artifact.obj

    if len(melody) < 2:
        raise Exception("Sequence length cannot be less than 2")

    S = _get_intervals(melody)
    mu = _get_mu(melody, S)
    RES = (2 * mu) / len(melody)
    if RES < 1.0:
        return RES
    else:
        return 1.0


def _get_mu(melody, S):
    c = 0
    for s in S:
        c = c + _count_s(melody, s)
    return (1 / len(S)) * c


def _get_intervals(melody):
    S = []
    for i in range(len(melody) - 1):
        new_interval = [melody[i][0], melody[i + 1][0]]
        S.append(new_interval)
    return S


def _count_s(melody, S):
    count = 0
    for i in range(len(melody) - 1):
        if S[0] == melody[i][0] and S[1] == melody[i + 1][0]:
            count += 1
    return count


def delete_outputs(folder):
    """
    Deletes the all contents in the folder, does not remove folder
    """
    if not os.path.exists(folder):
        os.makedirs(folder)

    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

def sequence_to_stream(sequence):
    s = stream.Stream()
    for i in range(len(sequence)):
        n = note.Note(sequence[i][0])
        n.quarterLength = sequence[i][1]
        s.append(n)
    return s

def get_instruments():
    """
    Returns the instrument list from a csv file
    :return: instrument list
    """
    numpy_data = genfromtxt('midi-instruments.csv', delimiter=',', dtype='U13')
    instrument_list = numpy_data.tolist()
    return instrument_list

def instrument_family(instrument_list, family_name = 'sound_effects'):
    """
    Returns instrument number by family name
    :param family_name: Family name of the instrument

                        List of families in the file
                        piano, chromatic_percussion, organ,
                        guitar, bass, strings, ensemble,
                        brass, reed, pipe, synth_lead, synth_pad,
                        synth_effects, ethnic, percussive, sound_effects

    :return: Returns random instrument number by family names
    """
    candidates = list()
    for i in instrument_list:
        # 4th column is family name
        if i[3] == family_name:
            candidates.append(i)

    if len(candidates) < 1:
        raise Exception("Write a valid family name")

    return int(random.choice(candidates)[0])

def change_instrument(stream, number):
    """
    Changes instrument of the given stream.

    :param stream: music21 Stream object
    :param number: Instrument number see the midi-instrument.csv for more detail
    """
    if number < 0 or number > 127:
        raise Exception("Invalid instrument")

    i = instrument.Instrument()
    i.midiProgram = number
    stream.insert(0, i)
