from GOAP.agent import GOAPAgent
from GOAP.providable import GOAPProvidable
from GOAP.action_set import ActionSet

# Actions
from GOAP.Actions.Worker.gather_logs import GatherLogs
from GOAP.Actions.Worker.gather_ore import GatherOre
from GOAP.Actions.Worker.deliver_logs import DeliverLogs
from GOAP.Actions.Worker.deliver_ore import DeliverOre

class Worker(GOAPAgent, GOAPProvidable):

    def __init__(self):
        super().__init__()
        self.data_provider = self
        self.goal_state = None
        
        # local variables
        self.backpack = []

        # actions
        self.add_action(GatherLogs())
        self.add_action(GatherOre())
        self.add_action(DeliverLogs())
        self.add_action(DeliverOre())

    def create_world_state(self):
        # Returns an evaluated set of the world state
        world_data = {}
        #
        world_data["hasOre"] = self.backpack.count("Ore") > 0
        world_data["hasLogs"] = self.backpack.count("Logs") > 0
        #
        return world_data

    def create_goal_state(self):
        if self.goal_state:
            return self.goal_state
        
        goal_state = ActionSet()
        goal_state.add("isIdle", True)

        return goal_state
