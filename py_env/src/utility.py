import os, shutil
from music21 import *
from numpy import genfromtxt
import random
from math import factorial

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

def sequence_to_part(sequence):
    p = stream.Part()
    for i in range(len(sequence)):
        n = note.Note(sequence[i][0])
        n.quarterLength = sequence[i][1]
        p.append(n)
    return p

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


def zipfs_law(artifact):
    """
    Calculates the value of an artifact using Zipf's law.
    In this method, it is assumed that music notes follow the Zipf's Law, in which
    the second most frequent pitch is 1/2 as frequent as the first, the third is
    1/3 as frequent as the first, etc. In this function we compare the actual probabilities
    with the expected probabilities and we return the mean of relative differences
    between these two values.

    Args:
        artifact: an Artifact to be evaluated.

    Returns:
        a value between 0 and 1 indicating the value of the artifact.
    """

    artf = artifact.obj
    # make a list of note frequencies
    # print("Value artefact obj : {}".format(artf))
    incidence_table = {}
    for tune in artf:
        element = tune[0]
        if element not in incidence_table:
            incidence_table[element] = 1
        else:
            incidence_table[element] += 1
    sorted_incid_keys = sorted(incidence_table, key=incidence_table.get, reverse=True)
    sorted_incid_values = []
    for key in sorted_incid_keys:
        sorted_incid_values.append(incidence_table[key])

    total = sum(sorted_incid_values)
    sorted_frequencies = []
    # here it is
    for value in sorted_incid_values:
        sorted_frequencies.append(value / total)

    # list of expected frequencies
    n = len(sorted_frequencies)
    numerator = factorial(n)
    denominator = 0
    for i in range(1, n + 1):
        denominator += numerator / i

    # code that retrieves expected probabilities/frequencies
    most_frequent_tune_prob = numerator / denominator
    expected_frequencies = []
    for i in range(1, n + 1):
        expected_frequencies.append(most_frequent_tune_prob / i)
    pseudo_fit_parts = []

    for i in range(len(sorted_frequencies)):
        diff = abs(sorted_frequencies[i] - expected_frequencies[i])
        ratio = 1 - (diff / expected_frequencies[i])
        pseudo_fit_parts.append(ratio)

    pseudo_fit = 0
    for value in pseudo_fit_parts:
        pseudo_fit += value
    pseudo_fit = pseudo_fit / len(sorted_frequencies)

    return pseudo_fit

def transpose(strm, step):
    #TODO: this is still transposing to another key, it would be great to transpose but
    #to keep things in C major.
    """
    Transposes the stream into the key given by step.
    Args:
        strm: Stream of music21
        step: (int) index of the key to be transposed to

    Returns:
        a transposed version Stream of strm.

    """
    return strm.transpose(step)

def inverse(strm):
    """
    Inverses the stream. Each step up is converted into a step down and vice-versa.

    Args:
        strm: Stream of music21
        step: (int) index of the key to be transposed to

    Returns:
        an inversed version Stream of strm.

    """

    return strm.invertDiatonic(note.Note(0), inPlace=False)

def retrograde(strm):
    """
    Retrogrades the stream. The notes at the end come to the begining and vice-versa.

    Args:
        strm: Stream of music21

    Returns:
        a retrograde version Stream of strm.

    """
    retrograded=stream.Stream()
    l=[]
    for note in strm:
        l.append(note)
    for note in reversed(l):
        retrograded.append(note)

    return retrograded

def inverse_and_retrograde(strm):
    """
    Retrogrades and inverses the stream.

    Args:
        strm: Stream of music21

    Returns:
        a retrograde version Stream of strm.

    """

    return inverse(retrograde(strm))