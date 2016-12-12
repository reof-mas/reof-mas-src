from creamas import CreativeAgent
import aiomas
import utility


class AudienceAgent(CreativeAgent):

    def __init__(self, env):
        super().__init__(env)

    @aiomas.expose
    async def give_opinion(self, artifact):
        """
        Gives an uneducated opinion about an artifact.

        Arguments:
            artifact: artifact to be evaluated
        Returns:
            opinion about an artifact
        """
        return utility.zipfs_law(artifact)

    async def act(self):
        """
        Does nothing.
        """
        return
