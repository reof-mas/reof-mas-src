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
    from music21 import interval, note

    steps = []
    for i in range(len(melody)-1):
        note1 = melody[i]
        note2 = melody[i + 1]
        steps.append(interval.notesToChromatic(note.Note(note1[0]), note.Note(note2[0])).intervalClass)

    return steps