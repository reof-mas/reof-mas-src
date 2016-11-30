def get_markov_chain(filePath):
    import music21 as m

    song = m.converter.parse(filePath)

    # Get the notes using generator expression
    notes = [note for note in song[0] if type(note) is m.note.Note]

    # Compute number of transitions
    transitions = {}
    for i in range(len(notes) - 1):
        # A state is represented as a note and duration
        pred = (notes[i].name, notes[i].duration.quarterLength)
        succ = (notes[i + 1].name, notes[i + 1].duration.quarterLength)

        if pred not in transitions:
            transitions[pred] = {}

        if succ not in transitions[pred]:
            transitions[pred][succ] = 1.0
        else:
            transitions[pred][succ] += 1.0

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
