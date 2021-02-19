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
        Metallurgist = auto()

# Actions
from GOAP.Actions.Artisan.pickup_builder_job import PickupBuilderJob
from GOAP.Actions.Artisan.pickup_refiner_job import PickupRefinerJob
from GOAP.Actions.Artisan.pickup_metallurgist_job import PickupMetallurgistJob
from GOAP.Actions.Artisan.pickup_smith_job import PickupSmithJob

class Artisan(GOAPAgent, GameActor, GOAPProvidable):

    def __init__(self):
        GOAPAgent.__init__(self)
        self.data_provider = self
        self.tile_color = g_vars["Unit"]["Artisan"]["TileColor"]
        self.image = Surface((g_vars["Game"]["UnitSize"], g_vars["Game"]["UnitSize"]))
        GameActor.__init__(self)
        
        # local variables
        self.profession = None

        # actions
        self.add_action(PickupBuilderJob())
        self.add_action(PickupRefinerJob())
        self.add_action(PickupMetallurgistJob())
        self.add_action(PickupSmithJob())

    def create_world_state(self):
        # Returns an evaluated set of the world state
        world_data = {}
        #
        world_data["isRefiner"] = self.profession == Profession.Refiner
        world_data["isSmith"]   = self.profession == Profession.Smith
        world_data["isBuilder"] = self.profession == Profession.Builder
        world_data["isMetallurgist"] = self.profession == Profession.Metallurgist
        #
        return world_data

    def create_goal_state(self):       
        goal_state = ActionSet()
        goal_state.add("doJob", True)

        return goal_state

    def update(self):
        GOAPAgent.update(self)
        GameActor.update(self)
