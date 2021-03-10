from pygame import Surface

from game_settings import g_vars

from GOAP2.__entity import __Entity

class Worker(__Entity):

    def __init__(self) -> None:
        # Sprite
        self.tile_color = g_vars["Unit"]["Worker"]["TileColor"]
        self.image = Surface((g_vars["Game"]["UnitSize"], g_vars["Game"]["UnitSize"]))
        super().__init__()

        self.goals = ["CollectResources", "FindResources", "BeUpgraded", "TransferResources"] 
        self.available_actions = ["GatherOre", "GatherLogs", "DeliverOre", "DeliverLogs", "FindLogs", "FindOre", "PickupFetchJob", "FetchResource", "PickupUpgradeJob"]
