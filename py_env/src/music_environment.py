from creamas import Environment
import logging
from music21 import *


class MusicEnvironment(Environment):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.save_iter = 3

    def vote(self, age):
        artifacts = self.perform_voting(method='mean')
        if len(artifacts) > 0:
            accepted = artifacts[0][0]
            value = artifacts[0][1]
            self.add_artifact(accepted)
            self.write_midi(accepted.obj, 'outputs/artefact_'+str(age)+'.mid', age)
            self.logger.log(logging.INFO, "Vote winner by {}: {} (val={})"
                        .format(accepted.creator, accepted.obj, value))
        else:
            self.logger.log(logging.INFO, "No vote winner!")

        self.clear_candidates()

    def write_midi(self, sequence, filename, age=-1):
        def _write_midi(sequence, filename):
            s = stream.Stream()
            for i in range(len(sequence)):
                n = note.Note(sequence[i][0])
                n.quarterLength = sequence[i][1]
                s.append(n)
            # write into the file
            s.write('midi', filename)

        if age == -1:
            _write_midi(sequence, filename)
        else:
            if (age % self.save_iter) == 0:
                _write_midi(sequence, filename)