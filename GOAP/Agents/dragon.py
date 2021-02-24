from pygame import Surface

from game_settings import g_vars
import game_time as time

from GOAP.action_set import ActionSet
from GOAP.agent import GOAPAgent
from GOAP.game_actor import GameActor
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

class Dragon(GOAPAgent, GameActor, GOAPProvidable):

    def __init__(self):
        GOAPAgent.__init__(self)
        self.data_provider = self
        self.tile_color = g_vars["Unit"]["Soldier"]["TileColor"]
        self.image = Surface((g_vars["Game"]["UnitSize"], g_vars["Game"]["UnitSize"]))
        GameActor.__init__(self)

        # overrides
        self.move_factor = 4

        # local variables
        self.position = Position(3, 1)
        self.home = Position(3, 1)
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
        GOAPAgent.update(self)
        GameActor.update(self)
        self.hunger += 2.0 * time.clock.delta
        self.social += 1.0 * time.clock.delta
        self.boredom += 3.0 * time.clock.delta

    def create_world_state(self):
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
