from pygame import sprite
from pygame import Surface

import game_settings as settings
import game_assets as assets


class Forest(sprite.Sprite):
    def __init__(self, gamemap, x, y):
        self.groups = gamemap.sprite_group_all
        sprite.Sprite.__init__(self, self.groups) # Add self to group
        self.gamemap = gamemap
        #self.image = assets.LoadSprite("unicorn.jpg")
        self.image = Surface((settings.TILE_SIZE, settings.TILE_SIZE))
        self.image.fill(settings.COLOR["FOREST"])
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        
        # can be moved into update 
        self.rect.x = x * settings.TILE_SIZE
        self.rect.y = y * settings.TILE_SIZE

class Ground(sprite.Sprite):
    def __init__(self, gamemap, x, y):
        self.groups = gamemap.sprite_group_all
        sprite.Sprite.__init__(self, self.groups) # Add self to group
        self.gamemap = gamemap
        self.image = Surface((settings.TILE_SIZE, settings.TILE_SIZE))
        self.image.fill(settings.COLOR["GROUND"])
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        
        self.rect.x = x * settings.TILE_SIZE
        self.rect.y = y * settings.TILE_SIZE

class Water(sprite.Sprite):
    def __init__(self, gamemap, x, y):
        self.groups = gamemap.sprite_group_all
        sprite.Sprite.__init__(self, self.groups) # Add self to group
        self.gamemap = gamemap
        self.image = Surface((settings.TILE_SIZE, settings.TILE_SIZE))
        self.image.fill(settings.COLOR["WATER"])
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        
        self.rect.x = x * settings.TILE_SIZE
        self.rect.y = y * settings.TILE_SIZE

class Bog(sprite.Sprite):
    def __init__(self, gamemap, x, y):
        self.groups = gamemap.sprite_group_all
        sprite.Sprite.__init__(self, self.groups) # Add self to group
        self.gamemap = gamemap
        self.image = Surface((settings.TILE_SIZE, settings.TILE_SIZE))
        self.image.fill(settings.COLOR["BOG"])
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        
        self.rect.x = x * settings.TILE_SIZE
        self.rect.y = y * settings.TILE_SIZE

class Mountain(sprite.Sprite):
    def __init__(self, gamemap, x, y):
        self.groups = gamemap.sprite_group_all
        sprite.Sprite.__init__(self, self.groups)
        self.gamemap = gamemap
        self.image = Surface((settings.TILE_SIZE, settings.TILE_SIZE))
        self.image.fill(settings.COLOR["MOUNTAIN"])
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * settings.TILE_SIZE
        self.rect.y = y * settings.TILE_SIZE