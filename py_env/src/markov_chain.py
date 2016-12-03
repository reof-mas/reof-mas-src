def get_markov_chain(filePath, order=1):
    '''
    Creates markov chain from midi file.

    :param filePath:
        Path of the midi file
    :param order:
        Order of the markov chain
    :return:
        Transition probabilities
    '''
    import music21 as m

    s = m.converter.parse(filePath)

    # transpose the melody to C
    k = s.analyze("key")
    i = m.interval.Interval(k.tonic, m.pitch.Pitch("C"))
    song = s.transpose(i)

    # Get the notes using generator expression
    notes = [note for note in song[0] if type(note) is m.note.Note]

    states = _get_states(notes, order)

    transitions = _get_transition_counts(states)

    # Compute total number of successors for each state
    totals = {}
    for pred, succ_counts in transitions.items():
        totals[pred] = sum(succ_counts.values())

    # Compute the probability for each successor given the predecessor.
    probs = {}
    for pred, succ_counts in transitions.items():
        probs[pred] = {}
        for succ, count in succ_counts.items():
            probs[pred][succ] = count / totals[pred]

    return probs

def _get_states(notes, order = 1):
    '''
    Extracts states from notes.

    :param notes:
        The noves where the states are extracted
    :param order:
        Order of the markov chain
    :return:
        The states extracted from the notes
    '''
    import warnings

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

def _get_transition_counts(states):
    '''
    Computes transition counts of states

    :param states:
        The states of the markov chain
    :return:
        Transition counts
    '''
    transitions = {}
    for i in range(len(states) - 1):
        # A state is represented as a note and duration
        pred = states[i]
        succ = states[i+1]

        if pred not in transitions:
            transitions[pred] = {}

        if succ not in transitions[pred]:
            transitions[pred][succ] = 1.0
        else:
            transitions[pred][succ] += 1.0

    return transitions
