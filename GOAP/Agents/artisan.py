from enum import Enum, auto
from pygame import Surface

from game_settings import g_vars

from GOAP.agent import GOAPAgent
from GOAP.providable import GOAPProvidable
from GOAP.action_set import ActionSet
from GOAP.game_actor import GameActor

class Profession(Enum):
        Refiner = auto()
        Smith = auto()
        Builder = auto()
        Smelter = auto()

# Actions
from GOAP.Actions.Artisan.build_structure import BuildStructure

class Artisan(GOAPAgent, GameActor, GOAPProvidable):

    def __init__(self):
        GOAPAgent.__init__(self)
        self.data_provider = self
        self.tile_color = g_vars["Unit"]["Artisan"]["TileColor"]
        self.image = Surface((g_vars["Game"]["UnitSize"], g_vars["Game"]["UnitSize"]))
        GameActor.__init__(self)
        self.position.x = 1
        self.position.y = 2
        
        # local variables
        self.goal_state = None
        self.profession = Profession.Builder

        # actions
        self.add_action(BuildStructure())

    def create_world_state(self):
        # Returns an evaluated set of the world state
        world_data = {}
        #
        world_data["isRefiner"] = self.profession == Profession.Refiner
        world_data["isSmith"]   = self.profession == Profession.Smith
        world_data["isBuilder"] = self.profession == Profession.Builder
        world_data["isSmelter"] = self.profession == Profession.Smelter
        #
        return world_data

    def create_goal_state(self):        
        if self.goal_state:
            return self.goal_state
        
        goal_state = ActionSet()
        goal_state.add("isIdle", True)

        return goal_state

    def update(self):
        GOAPAgent.update(self)
        GameActor.update(self)
