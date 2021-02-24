from pygame import Surface

from game_settings import g_vars

from GOAP.agent import GOAPAgent
from GOAP.game_actor import GameActor
from GOAP.providable import GOAPProvidable
from GOAP.action_set import ActionSet
from GOAP.transform import Position

# Actions
from GOAP.Actions.DragonKeeper.fish_for_dragon import FishForDragon
from GOAP.Actions.DragonKeeper.hunt_for_dragon import HuntForDragon
from GOAP.Actions.DragonKeeper.feed_dragon import FeedDragon

class DragonKeeper(GOAPAgent, GameActor, GOAPProvidable):

    def __init__(self, dragon):
        GOAPAgent.__init__(self)
        self.data_provider = self
        self.tile_color = g_vars["Unit"]["Worker"]["TileColor"]
        self.image = Surface((g_vars["Game"]["UnitSize"], g_vars["Game"]["UnitSize"]))
        GameActor.__init__(self)

        # local variables
        self.dragon = dragon
        self.position = Position(3, 3)
        self.backpack = []

        # actions
        self.add_action(FishForDragon())
        self.add_action(HuntForDragon())
        self.add_action(FeedDragon())

    def update(self):
        GOAPAgent.update(self)
        GameActor.update(self)

    def create_world_state(self):
        # Returns an evaluated set of the world state
        world_data = {}
        #
        world_data["dragonIsHungry"] = self.dragon.create_world_state()["isHungry"]
        world_data["dragonIsHome"] = self.dragon.create_world_state()["isHome"]
        world_data["hasMeat"] = self.backpack.count("Meat") > 0
        #
        return world_data

    def create_goal_state(self):
        goal_state = ActionSet()
        goal_state.add("satisfyDragon", True)

        return goal_state
