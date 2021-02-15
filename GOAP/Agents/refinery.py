from pygame import Surface
from random import randint

from game_settings import g_vars

from GOAP.agent import GOAPAgent
from GOAP.providable import GOAPProvidable
from GOAP.action_set import ActionSet
from GOAP.game_actor import GameActor

# Actions
from GOAP.Actions.Structures.produce_coal import ProduceCoal
from GOAP.Actions.Structures.call_builder import CallBuilder

class Refinery(GOAPAgent, GameActor, GOAPProvidable):

    def __init__(self):
        GOAPAgent.__init__(self)
        self.data_provider = self
        self.tile_color = g_vars["Structure"]["Base"]["TileColor"]
        self.image = Surface((g_vars["Game"]["StructureSize"], g_vars["Game"]["StructureSize"]))
        GameActor.__init__(self)
        self.position.x = randint(1, 6)
        self.position.y = randint(1, 6)
        
        # local variables
        self.inventory = []
        self.is_built = False

        # actions
        self.add_action(ProduceCoal())
        self.add_action(CallBuilder())

    def create_world_state(self):
        # Returns an evaluated set of the world state
        world_data = {}
        #
        world_data["isBuilt"] = self.is_built
        #world_data["isWorked"] = artisan working on it
        #
        return world_data

    def create_goal_state(self):        
        goal_state = ActionSet()
        goal_state.add("hasCoal", True)

        return goal_state

    def update(self):
        GOAPAgent.update(self)
        GameActor.update(self)

    def on_built(self):
        self.is_built = True
        self.tile_color = g_vars["Structure"]["Refinery"]["TileColor"]
        self.image.fill(g_vars["Game"]["Colors"][self.tile_color])
        print("Refinery built!")
