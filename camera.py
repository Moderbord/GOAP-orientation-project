from pygame import Rect
from pygame.mouse import get_pos

from game_settings import g_vars

class Camera:
    def __init__(self):
        self.camera = None
        self.width = 0
        self.height = 0
        self.x = 0
        self.y = 0

    def set_resolution(self, width, height):
        self.camera = Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def move(self, dx=0, dy=0):
        self.x += dx * int(g_vars["Game"]["TileSize"])
        self.y += dy * int(g_vars["Game"]["TileSize"])
        self.camera = Rect(-self.x, -self.y, self.width, self.height)

camera = Camera()