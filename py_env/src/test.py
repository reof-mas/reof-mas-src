from composer import ComposerAgent
import markov_chain
from music_environment import MusicEnvironment
from music21 import *

env = MusicEnvironment.create(('localhost', 5555))
composer = ComposerAgent(env, markov_chain.get_markov_chain('../../melodies/popular/duke_ellington/MPG9GXQU.mid'))

melody = composer.generate()

score1 = converter.parse('../../melodies/popular/duke_ellington/MPG9GXQU.mid')
#score1.show('text')

s1 = stream.Stream()
key = key.Key('C')
s1.append(key)

for state in melody.obj:
    asd = note.Note(state[0])
    asd.quarterLength = state[1]
    s1.append(asd)

s1.show('text')
#environment.set('midiPath', '/usr/bin/timidity')
s1.show('midi')