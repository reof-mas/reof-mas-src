import warnings
import music21 as m
import os

def get_markov_chain(directory_path, order=1):
    """
    Creates markov chain from midi file.

    :param file_path:
        Path of the midi file
    :param order:
        Order of the markov chain
    :return:
        Transition probabilities
    """


    # Get midi files from directory_path
    files = os.listdir(directory_path)
    midi_files = [file for file in files if os.path.splitext(file)[1] == '.mid']

    transitions = {}

    # Calculate transition counts using all the files in directory_path
    for file in midi_files:
        # Create the full filepath of the midi file
        file_path = directory_path
        if directory_path[-1] !=  os.sep:
            file_path += os.sep
        file_path += file

        s = m.converter.parse(file_path)

        # transpose the melody to C
        k = s.analyze("key")
        i = m.interval.Interval(k.tonic, m.pitch.Pitch("C"))
        song = s.transpose(i)

        # Get the notes using generator expression
        notes = [note for note in song[0] if type(note) is m.note.Note]

        if len(notes) == 0:
            warnings.warn("Couldn't read notes in file: {}".format(file_path))
        else:
            states = _get_states(notes, order)
            transitions = _add_transitions(states, transitions)

    return transitions


def get_transitions_probs_for_state(succ_counts):
    total = sum(succ_counts.values())
    succ_probs = {}
    for succ, count in succ_counts.items():
        succ_probs[succ] = count / total

    return succ_probs


def _get_states(notes, order = 1):
    """
    Extracts states from notes.

    :param notes:
        The noves where the states are extracted
    :param order:
        Order of the markov chain
    :return:
        The states extracted from the notes
    """
    states = []
    i = 0

    if len(notes) < order:
        warnings.warn('Markov chain order is larger than the amount of notes in melody')
        return states

    while i+order-1 < len(notes):
        state = []
        for j in range(order):
            state.append((notes[i+j].name, notes[i+j].duration.quarterLength))
        states.append(tuple(state))
        i += 1

    return states

def _add_transitions(states, transitions):
    """
    Computes transition counts of states

    :param states:
        The states of the markov chain
    :param transitions:
        Adds state transitions from states to transitions
    :return:
        Transition counts
    """
    for i in range(len(states) - 1):
        # A state is represented as a note and duration
        pred = states[i]
        succ = states[i+1]

        if pred not in transitions:
            transitions[pred] = {}

        if succ not in transitions[pred]:
            #print("new state added : {} {}".format(pred,succ))
            transitions[pred][succ] = 1.0
        else:
            #print("Increment state : {} {}".format(pred, succ))
            transitions[pred][succ] += 1.0

    return transitions
