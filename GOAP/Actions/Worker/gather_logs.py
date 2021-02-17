from GOAP.Actions.Worker.gather_action import GatherAction

class GatherLogs(GatherAction):

    def __init__(self):
        super().__init__()
        self.target_resource = "Logs"
        self.message_on_finish = "chopped wood."

        self.duration = 5

    def get_cost(self, agent):
        return self.cost + agent.owner.logs_gatherers + agent.owner.resources.count(self.target_resource)

    def on_start(self, agent):
        super().on_start(agent)
        agent.owner.logs_gatherers += 1

    def on_end(self, agent):
        agent.owner.logs_gatherers -= 1