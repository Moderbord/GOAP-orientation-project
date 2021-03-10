from pygame import Surface

from game_settings import g_vars

from GOAP.transform import Position
from GOAP2.__entity import __Entity

class Camp(__Entity):

    def __init__(self) -> None:
        # Sprite
        self.tile_color = g_vars["Structure"]["Camp"]["TileColor"]
        self.image = Surface((g_vars["Game"]["StructureSize"], g_vars["Game"]["StructureSize"]))
        super().__init__()

        self.position = Position(2, 2)

        self.goals = ["ProduceUnits"]
        self.available_actions = ["ProduceArtisan"]
