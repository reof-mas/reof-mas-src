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
                new[i].accidental=acc
                has_accidental=True
        if has_accidental is False:
            new[i].accidental=0
    return new

l=[]
l.append(note.Note("C4"))
l.append(note.Note("D4"))
l.append(note.Note("E4"))
l.append(note.Note("F4"))
l.append(note.Note("G4"))
l.append(note.Note("A4"))
l.append(note.Note("B4"))

s=stream.Stream()
s.append(l)

k=key.Key("C")
t=diatonic_transposition(s, "3m", k)

s.show()
t.show()