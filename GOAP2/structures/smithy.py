from pygame import Surface

from game_settings import g_vars

from GOAP2.__entity import __Entity

class Smithy(__Entity):

    def __init__(self) -> None:
        # Sprite
        self.tile_color = g_vars["Structure"]["Base"]["TileColor"]
        self.image = Surface((g_vars["Game"]["StructureSize"], g_vars["Game"]["StructureSize"]))
        super().__init__()

        self.goals = ["GetBuilt", "GetWorked", "ProduceSword"]
        self.available_actions = ["CreateBuildJob", "CreateFetchJob", "CreateWorkJob", "ProduceSword"]
