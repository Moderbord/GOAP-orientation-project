import game_time as time

from GOAP.action_set import ActionSet
from GOAP.agent import GOAPAgent
from GOAP.providable import GOAPProvidable
from GOAP.transform import Position
from GOAP.transform import distance

# Actions
from GOAP.Actions.Dragon.eat_meat import EatMeat
from GOAP.Actions.Dragon.burn_subject import BurnSubject
from GOAP.Actions.Dragon.survey_territory import SurveyTerritory
from GOAP.Actions.Dragon.return_home import ReturnHome
from GOAP.Actions.Dragon.wait_for_meat import WaitForMeat
from GOAP.Actions.Dragon.hunt_for_meat import HuntForMeat

class Dragon(GOAPAgent, GOAPProvidable):

    def __init__(self):
        super().__init__()
        self.data_provider = self

        # overrides
        self.move_threshold = 1.0/4.0

        # local variables
        self.position = Position(3, 0)
        self.home = Position(3, 0)
        self.backpack = []
        self.health = 100
        self.hunger = 0
        self.social = 10
        self.boredom = 25
        self.subjects = 2

        # flags
        self.waited_for_food = False

        # actions
        self.add_action(EatMeat())
        self.add_action(BurnSubject())
        self.add_action(SurveyTerritory())
        self.add_action(ReturnHome())
        self.add_action(WaitForMeat())
        self.add_action(HuntForMeat())
    
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
        world_data["isHungry"] = self.hunger > 20
        world_data["isLonely"] = self.social > 20
        world_data["isBored"] = self.boredom > 20
        #
        world_data["hasWaited"] = self.waited_for_food
        world_data["hasMeat"] = self.backpack.count("Meat") > 0
        world_data["isHome"] = distance(self.position, self.home) <= 0
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
