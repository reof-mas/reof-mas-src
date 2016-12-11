from creamas import CreativeAgent
import aiomas
import utility


class AudienceAgent(CreativeAgent):

    def __init__(self, env):
        super().__init__(env)

    def opinion(self, artifact):
        return utility.zipfs_law(artifact)

    @aiomas.expose
    async def give_opinion(self, artifact):
        return self.opinion(artifact)

    async def act(self):
        return