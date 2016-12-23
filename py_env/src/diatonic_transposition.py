from music21 import *

def diatonic_transposition(stm, interval, k):
    new=stm.transpose(interval)
    l=[]
    for ptc in k.alteredPitches:
        l.append((ptc.name[0], ptc.name[1:]))
    for i in range(len(new)):
        n=new[i].name
        has_accidental=False
        for m, acc in l:
            if n is m:
                new[i].accidental.set(acc)
                has_accidental=True
        if has_accidental is False:
            new[i].accidental.set(0)
    return new

l=[]
l.append(note.Note("C"))
l.append(note.Note("D"))
l.append(note.Note("E"))
l.append(note.Note("F"))
l.append(note.Note("G"))
l.append(note.Note("A"))
l.append(note.Note("B"))

s=stream.Stream()
s.append(l)

k=key.Key("D")
t=diatonic_transposition(s, "3m", k)

s.show()
t.show()