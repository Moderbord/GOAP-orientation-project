from GOAP.transform import Position
from pygame import Surface

from game_settings import g_vars

from GOAP.agent import GOAPAgent
from GOAP.providable import GOAPProvidable
from GOAP.game_actor import GameActor
from GOAP.Agents.artisan import Artisan

# Actions

class Camp(GOAPAgent, GameActor, GOAPProvidable):

    def __init__(self):
        GOAPAgent.__init__(self)
        self.data_provider = self
        self.tile_color = g_vars["Structure"]["Camp"]["TileColor"]
        self.image = Surface((g_vars["Game"]["StructureSize"], g_vars["Game"]["StructureSize"]))
        GameActor.__init__(self)
        self.position = Position(2, 2)
        
        # local variables

        # actions

    def create_world_state(self):
        # Returns an evaluated set of the world state
        world_data = {}
        #
        #
        return world_data

    def create_goal_state(self):        
        goal_state = {}
        return goal_state

    def update(self):
        GOAPAgent.update(self)
        GameActor.update(self)

    def on_upgrade(self, target_profession):
        new_artisan = Artisan()
        new_artisan.profession = target_profession
        new_artisan.position = Position(self.position.x, self.position.y)
        self.owner.add_unit(new_artisan)
