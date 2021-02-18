from pygame import Surface

from game_settings import g_vars

from GOAP.agent import GOAPAgent
from GOAP.providable import GOAPProvidable
from GOAP.action_set import ActionSet
from GOAP.game_actor import GameActor

# Actions
from GOAP.Actions.Worker.gather_logs import GatherLogs
from GOAP.Actions.Worker.gather_ore import GatherOre
from GOAP.Actions.Worker.pickup_collect_job import PickupCollectJob
from GOAP.Actions.Worker.pickup_fetch_job import PickupFetchJob
from GOAP.Actions.Worker.pickup_upgrade_job import PickupUpgradeJob

class Worker(GOAPAgent, GameActor, GOAPProvidable):

    def __init__(self):
        GOAPAgent.__init__(self)
        self.data_provider = self
        self.tile_color = g_vars["Unit"]["Worker"]["TileColor"]
        self.image = Surface((g_vars["Game"]["UnitSize"], g_vars["Game"]["UnitSize"]))
        GameActor.__init__(self)
        
        # local variables
        self.backpack = []

        # actions
        self.add_action(GatherLogs())
        self.add_action(GatherOre())
        self.add_action(PickupFetchJob())
        self.add_action(PickupCollectJob())
        self.add_action(PickupUpgradeJob())

    def create_world_state(self):
        # Returns an evaluated set of the world state
        world_data = {}
        #
        world_data["hasOre"] = self.backpack.count("Ore") > 0
        world_data["hasLogs"] = self.backpack.count("Logs") > 0
        #
        return world_data

    def create_goal_state(self):        
        goal_state = ActionSet()
        goal_state.add("doJob", True)

        return goal_state

    def update(self):
        GOAPAgent.update(self)
        GameActor.update(self)
