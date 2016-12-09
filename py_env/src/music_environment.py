from creamas import Environment
import logging


class MusicEnvironment(Environment):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def vote(self, age):
        artifacts = self.perform_voting(method='mean')
        if len(artifacts) > 0:
            accepted = artifacts[0][0]
            value = artifacts[0][1]
            self.add_artifact(accepted)
            self.logger.log(logging.INFO, "Vote winner by {}: {} (val={})"
                        .format(accepted.creator, accepted.obj, value))
        else:
            self.logger.log(logging.INFO, "No vote winner!")

        self.clear_candidates()