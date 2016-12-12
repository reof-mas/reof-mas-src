from creamas import Environment
import logging
from utility import *

class MusicEnvironment(Environment):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.save_iter = 1

    def vote(self, age):
        artifacts = self.perform_voting(method='mean')
        if len(artifacts) > 0:
            accepted = artifacts[0][0]
            value = artifacts[0][1]
            #print(self_similarity(accepted))
            self.add_artifact(accepted)
            self.write_midi(accepted.obj, 'outputs/artefact_'+str(age)+'.mid', age)
            self.logger.log(logging.INFO, "Vote winner by {}: {} (val={})"
                        .format(accepted.creator, accepted.obj, value))
        else:
            self.logger.log(logging.INFO, "No vote winner!")

        self.clear_candidates()

    def write_midi(self, sequence, filename, age=-1):
        def _write_midi(sequence, filename):
            strm = sequence_to_stream(sequence)
            # write into the file
            strm.write('midi', filename)

        if age == -1:
            _write_midi(sequence, filename)
        else:
            if (age % self.save_iter) == 0:
                _write_midi(sequence, filename)