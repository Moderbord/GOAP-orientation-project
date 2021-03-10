from pygame import Surface

from game_settings import g_vars

from GOAP2.__entity import __Entity

class Artisan(__Entity):

    def __init__(self) -> None:
        # Sprite
        self.tile_color = g_vars["Unit"]["Artisan"]["TileColor"]
        self.image = Surface((g_vars["Game"]["UnitSize"], g_vars["Game"]["UnitSize"]))
        super().__init__()

        self.goals = ["HaveProfession", "PerformArtisanWork"] 
        self.available_actions = ["PickProfession", "PickupBuildJob", "BuildStructure"]
