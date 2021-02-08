import game_time as time

from GOAP.action_set import ActionSet
from GOAP.agent import GOAPAgent
from GOAP.providable import GOAPProvidable
from GOAP.transform import Position

# Actions
from GOAP.Actions.Dragon.eat_meat import EatMeat
from GOAP.Actions.Dragon.burn_subject import BurnSubject

class Dragon(GOAPAgent, GOAPProvidable):

    def __init__(self):
        super().__init__()
        self.data_provider = self

        # overrides
        self.move_speed = 3

        # local variables
        self.position = Position(3, 0)
        self.backpack = []
        self.health = 100
        self.hunger = 0
        self.social = 10
        self.boredom = 25

        # actions
        self.add_action(EatMeat())
        self.add_action(BurnSubject())
    
    def update(self):
        super().update()
        self.hunger += 2.0 * time.clock.delta
        self.social += 1.0 * time.clock.delta
        self.boredom += 3.0 * time.clock.delta

    def get_world_state(self):
        # Returns an evaluated set of the world state
        world_data = {}
        #
        world_data["isAlive"] = self.health > 0
        world_data["isHungry"] = self.hunger > 50
        world_data["isLonely"] = self.social > 50
        world_data["isBored"] = self.boredom > 50
        #
        world_data["hasMeat"] = self.backpack.count("Meat") > 0
        #
        return world_data

    def create_goal_state(self):
        goal_state = ActionSet()
        goal_state.add("stayAlive", True)
        goal_state.add("staySatisfied", True)

        return goal_state

    def plan_failed(self, failed_goal):
        pass

    def plan_found(self, goal, actions):
        string = "Plan found: "
        tmp = actions.copy()
        while len(tmp) > 0:
            a = tmp.popleft()
            string += type(a).__name__
            string += " -> "
        print(string + str(goal))
        
    def actions_finished(self):
        pass

    def plan_aborted(self, aborted_action):
        print("Aborted plan: " + type(aborted_action).__name__)
