from pygame import Surface

from game_settings import g_vars

from GOAP2.agent import Agent

class Worker(Agent):

    def __init__(self) -> None:
        # Sprite
        self.tile_color = g_vars["Unit"]["Worker"]["TileColor"]
        self.image = Surface((g_vars["Game"]["UnitSize"], g_vars["Game"]["UnitSize"]))
        super().__init__()

        self.x = 2
        self.y = 2
        
        