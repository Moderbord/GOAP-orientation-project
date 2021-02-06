import GOAP.agent as agent
import GOAP.providable as providable

class Labourer(agent.GOAPAgent, providable.GOAPProvidable):

    def __init__(self):
        super().__init__()
        self.data_provider = self
        self.backpack = []
        self.move_speed = 1

    # def start(self):
    #     super().start()

    # def update(self):
    #     pass

    def get_world_state(self):
        # Returns an evaluated set of the world state
        
        world_data = {}
        world_data["hasOre"] = self.backpack.count("Ore") > 0
        world_data["hasLogs"] = self.backpack.count("Logs") > 0
        world_data["hasFirewood"] = self.backpack.count("Firewood") > 0
        return world_data

    def create_goal_state(self):
        pass

    def plan_failed(self, failed_goal):
        print("Plan failed")

    def plan_found(self, goal, actions):
        string = "Plan found: "
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

    def move_agent(self, next_action):
        
        if agent.transform.distance(self.position, next_action.target) <= next_action.minimun_range:
            next_action.set_in_range(True)
            return True
        else:
            # Move towards next action location
            self.position.x += self.move_speed if self.position.x < next_action.target.x else -self.move_speed
            self.position.y += self.move_speed if self.position.y < next_action.target.y else -self.move_speed

            print(type(self).__name__ + " moving to " + str(self.position.x) + " . " + str(self.position.y) + "...")
            return False