from pygame import sprite
from pygame import Surface

import game_settings as settings
import game_assets as assets

class BasicTile(sprite.Sprite):
    def __init__(self, gamemap, location):
        sprite.Sprite.__init__(self, self.groups) # Add self to group
        self.gamemap = gamemap
        # Grid coordinates
        self.location = location
        self.movement_factor = 1

        #self.image = assets.LoadSprite("unicorn.jpg")
        self.image = Surface((settings.TILE_SIZE, settings.TILE_SIZE))
        self.image.fill(settings.COLOR[self.tile_color])

        self.rect = self.image.get_rect()
        self.rect.x = location[0] * settings.TILE_SIZE
        self.rect.y = location[1] * settings.TILE_SIZE

class Fog(BasicTile):
    def __init__(self, gamemap, location):
        self.groups = gamemap.sprite_group_fog
        self.tile_color = "LIGHTGRAY"
        BasicTile.__init__(self, gamemap, location)

class Forest(BasicTile):
    def __init__(self, gamemap, location):
        self.groups = gamemap.sprite_group_background
        self.tile_color = "FOREST"
        BasicTile.__init__(self, gamemap, location)
        self.movement_factor = 0.8

class Ground(BasicTile):
    def __init__(self, gamemap, location):
        self.groups = gamemap.sprite_group_background
        self.tile_color = "GROUND"
        BasicTile.__init__(self, gamemap, location)

class Water(BasicTile):
    def __init__(self, gamemap, location):
        self.groups = gamemap.sprite_group_background
        self.tile_color = "WATER"
        BasicTile.__init__(self, gamemap, location)

class Bog(BasicTile):
    def __init__(self, gamemap, location):
        self.groups = gamemap.sprite_group_background
        self.tile_color = "BOG"
        BasicTile.__init__(self, gamemap, location)
        self.movement_factor = 0.5

class Mountain(BasicTile):
    def __init__(self, gamemap, location):
        self.groups = gamemap.sprite_group_background
        self.tile_color = "MOUNTAIN"
        BasicTile.__init__(self, gamemap, location)