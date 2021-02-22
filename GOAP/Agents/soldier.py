from pygame import Surface

from game_settings import g_vars

from GOAP.agent import GOAPAgent
from GOAP.providable import GOAPProvidable
from GOAP.action_set import ActionSet
from GOAP.game_actor import GameActor

# Actions
from GOAP.Actions.Explorer.explore import Explore

class Soldier(GOAPAgent, GameActor, GOAPProvidable):

    def __init__(self):
        GOAPAgent.__init__(self)
        self.data_provider = self
        self.tile_color = g_vars["Unit"]["Soldier"]["TileColor"]
        self.image = Surface((g_vars["Game"]["UnitSize"], g_vars["Game"]["UnitSize"]))
        GameActor.__init__(self)
        
        # local variables

        # actions
        self.add_action(Explore())

    def create_world_state(self):
        # Returns an evaluated set of the world state
        world_data = {}
        #
        return world_data

    def create_goal_state(self):        
        goal_state = ActionSet()
        goal_state.add("isExploring", True)

        return goal_state

    def update(self):
        GOAPAgent.update(self)
        GameActor.update(self)
