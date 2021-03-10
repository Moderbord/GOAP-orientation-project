from pygame import Surface

from game_settings import g_vars

from GOAP.transform import Position
from GOAP2.__entity import __Entity

class Worker(__Entity):

    def __init__(self) -> None:
        # Sprite
        self.tile_color = g_vars["Unit"]["Worker"]["TileColor"]
        self.image = Surface((g_vars["Game"]["UnitSize"], g_vars["Game"]["UnitSize"]))
        super().__init__()

        self.position = Position(2, 2)
        # TODO UpgradeToArtisan should just be Upgrade or smt, action should rather be UpgradeToArtisan
        # self.goals = ["CollectResources", "FindResources"] 
        self.goals = ["CollectResources", "FindResources", "UpgradeToArtisan", "TransferResources"] 
        self.available_actions = ["GatherOre", "GatherLogs", "DeliverOre", "DeliverLogs", "FindLogs", "FindOre", "PickupFetchJob", "DeliverResource"]
