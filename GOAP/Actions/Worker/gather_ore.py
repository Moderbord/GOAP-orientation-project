from GOAP.Actions.Worker.gather_action import GatherAction

class GatherOre(GatherAction):

    def __init__(self):
        super().__init__()
        self.target_resource = "Ore"
        self.message_on_finish = "mined ore."

        self.duration = 3
        
    def get_cost(self, agent):
        return self.cost + agent.owner.ore_gatherers + agent.owner.resources.count(self.target_resource)

    def on_start(self, agent):
        super().on_start(agent)
        agent.owner.ore_gatherers += 1

    def on_end(self, agent):
        agent.owner.ore_gatherers -= 1