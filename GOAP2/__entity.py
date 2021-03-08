from game_settings import g_vars

from GOAP.transform import Position

class __Entity():

    def __init__(self) -> None:
        # Sprite
        self.tile_size = g_vars["Game"]["TileSize"]
        self.image.fill(g_vars["Game"]["Colors"][self.tile_color])
        self.rect = self.image.get_rect()

        #
        self.position = Position(2, 2)

        # "XML"
        self.goals = []
        self.available_actions = []
        self.world_state = {}

    def set_position(self, position):
        self.position = position
        
    def update(self):
        # Sprite position
        self.rect.x = self.position.x * self.tile_size + self.tile_size / 3
        self.rect.y = self.position.y * self.tile_size + self.tile_size / 3

    def render(self, screen, camera):
        screen.blit(self.image, camera.apply(self))

