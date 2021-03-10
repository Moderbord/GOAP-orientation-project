from pygame import Surface

from game_settings import g_vars

from GOAP.transform import Position
from GOAP2.__entity import __Entity

class Refinery(__Entity):

    def __init__(self) -> None:
        # Sprite
        self.tile_color = g_vars["Structure"]["Base"]["TileColor"]
        self.image = Surface((g_vars["Game"]["StructureSize"], g_vars["Game"]["StructureSize"]))
        super().__init__()

        self.position = Position(4, 5)

        self.goals = ["GetBuilt"]
        self.available_actions = ["CreateBuildJob", "CreateFetchJob"]
