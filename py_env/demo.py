from music21 import *

#n = note.Note("D#3")
#n.duration.type = 'half'
#n.show('lily.pdf')

littleMelody = converter.parse("tinynotation: 3/4 c4 d8 f g16 a g f#")
littleMelody.show('lily')
littleMelody.show('midi')
littleMelody.write('midi', 'my_midi.mid')
print("Hello, I am the demonstration Python script")
