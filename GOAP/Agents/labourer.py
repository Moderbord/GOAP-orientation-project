from GOAP.agent import GOAPAgent
from GOAP.providable import GOAPProvidable

class Labourer(GOAPAgent, GOAPProvidable):

    def __init__(self):
        super().__init__()
        self.data_provider = self
        
        # local variables
        self.backpack = []

    def get_world_state(self):
        # Returns an evaluated set of the world state
        world_data = {}
        #
        world_data["hasOre"] = self.backpack.count("Ore") > 0
        world_data["hasLogs"] = self.backpack.count("Logs") > 0
        world_data["hasFirewood"] = self.backpack.count("Firewood") > 0
        #
        world_data["hasFood"] = self.backpack.count("Meat") > 0
        #
        return world_data

    def create_goal_state(self):
        pass

    def plan_failed(self, failed_goal):
        pass

    def plan_found(self, goal, actions):
        string = "(" + type(self).__name__ + ") Plan found: "
        tmp = actions.copy()
        while len(tmp) > 0:
            a = tmp.popleft()
            string += type(a).__name__
            string += " -> "
        print(string + str(goal))
        
    def actions_finished(self):
        print("Action finished!")

    def plan_aborted(self, aborted_action):
        print("Aborted plan: " + type(aborted_action).__name__)