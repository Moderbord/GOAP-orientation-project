from game_settings import g_vars

class Agent():

    def __init__(self) -> None:
        # Sprite
        self.tile_size = g_vars["Game"]["TileSize"]
        self.image.fill(g_vars["Game"]["Colors"][self.tile_color])
        self.rect = self.image.get_rect()

    def update(self):
        # Sprite position
        self.rect.x = self.x * self.tile_size + self.tile_size / 3
        self.rect.y = self.y * self.tile_size + self.tile_size / 3

    def render(self):
        pass

