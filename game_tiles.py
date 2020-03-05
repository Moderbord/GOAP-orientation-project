from pygame import sprite
from pygame import Surface

import game_settings as settings
import game_assets as assets


class TestExplorer(sprite.Sprite):
    def __init__(self, gamemap, x, y):
        self.groups = gamemap.sprite_group_all, gamemap.sprite_group_entities
        sprite.Sprite.__init__(self, self.groups) # Add self to group
        self.gamemap = gamemap
        # Grid coordinates
        self.x = x 
        self.y = y

        self.image = Surface((settings.TILE_SIZE, settings.TILE_SIZE))
        self.image.fill(settings.COLOR["RED"])
        self.rect = self.image.get_rect()

        self.move_speed = 3
        self.move_progress = 0

        self.current_path = None
        self.next_tile = None

    def get_position(self):
        return (self.x, self.y)

    def set_path(self, path):
        self.current_path = path
        self.next_tile = path[self.get_position()]

    def move(self, dx=0, dy=0):

        tile = (self.x + dx, self.y + dy)
        if tile in self.gamemap.unpassable_tiles:
            return

        self.x += dx
        self.y += dy

        # TODO clear 3x3 fog around entity on every move. prob is much cheaper

        x, y = self.x, self.y
        # remove fog dirty
        neighbors = [
            (x - 1, y - 1),
            (x + 0, y - 1),
            (x + 1, y - 1),

            (x - 1, y + 0),
            (x + 1, y + 0),

            (x - 1, y + 1),
            (x + 0, y + 1),
            (x + 1, y + 1),
        ]

        for neighbor in neighbors:
            if neighbor not in self.gamemap.cleared_fog:
                # add tile to explored list
                self.gamemap.cleared_fog.append(neighbor)
                # get fog tile
                tile = self.gamemap.get_fog_tile(neighbor)
                # remove
                sprite.Sprite.remove(tile, tile.groups)

    def update(self):
        
        # TODO take tile type into account
        # movement
        if self.current_path:

            (x1, y1) = self.get_position()
            (x2, y2) = self.next_tile
            dx = x2 - x1
            dy = y2 - y1

            self.move_progress += self.move_speed
            if self.move_progress >= 12:
                # reset progress
                self.move_progress = 0
                # move
                self.move(dx, dy)
                # update next tile
                self.next_tile = self.current_path[self.next_tile]
            
            if self.next_tile is None:
                self.current_path = None

        # drawing
        self.rect.x = self.x * settings.TILE_SIZE
        self.rect.y = self.y * settings.TILE_SIZE

class Fog(sprite.Sprite):
    def __init__(self, gamemap, x, y):
        self.groups = gamemap.sprite_group_fog
        sprite.Sprite.__init__(self, self.groups) # Add self to group
        self.gamemap = gamemap
        # Grid coordinates
        self.x = x 
        self.y = y

        #self.image = assets.LoadSprite("unicorn.jpg")
        self.image = Surface((settings.TILE_SIZE, settings.TILE_SIZE))
        self.image.fill(settings.COLOR["LIGHTGRAY"])

        self.rect = self.image.get_rect()
        self.rect.x = x * settings.TILE_SIZE
        self.rect.y = y * settings.TILE_SIZE

class Forest(sprite.Sprite):
    def __init__(self, gamemap, x, y):
        self.groups = gamemap.sprite_group_all
        sprite.Sprite.__init__(self, self.groups) # Add self to group
        self.gamemap = gamemap
        # Grid coordinates
        self.x = x 
        self.y = y

        #self.image = assets.LoadSprite("unicorn.jpg")
        self.image = Surface((settings.TILE_SIZE, settings.TILE_SIZE))
        self.image.fill(settings.COLOR["FOREST"])

        self.rect = self.image.get_rect()
        self.rect.x = x * settings.TILE_SIZE
        self.rect.y = y * settings.TILE_SIZE

class Ground(sprite.Sprite):
    def __init__(self, gamemap, x, y):
        self.groups = gamemap.sprite_group_all
        sprite.Sprite.__init__(self, self.groups) # Add self to group
        self.gamemap = gamemap
        self.x = x
        self.y = y

        self.image = Surface((settings.TILE_SIZE, settings.TILE_SIZE))
        self.image.fill(settings.COLOR["GROUND"])

        self.rect = self.image.get_rect()
        self.rect.x = x * settings.TILE_SIZE
        self.rect.y = y * settings.TILE_SIZE

class Water(sprite.Sprite):
    def __init__(self, gamemap, x, y):
        self.groups = gamemap.sprite_group_all
        sprite.Sprite.__init__(self, self.groups) # Add self to group
        self.gamemap = gamemap
        self.y = y
        self.x = x

        self.image = Surface((settings.TILE_SIZE, settings.TILE_SIZE))
        self.image.fill(settings.COLOR["WATER"])

        self.rect = self.image.get_rect()
        self.rect.x = x * settings.TILE_SIZE
        self.rect.y = y * settings.TILE_SIZE

class Bog(sprite.Sprite):
    def __init__(self, gamemap, x, y):
        self.groups = gamemap.sprite_group_all
        sprite.Sprite.__init__(self, self.groups) # Add self to group
        self.gamemap = gamemap
        self.x = x
        self.y = y

        self.image = Surface((settings.TILE_SIZE, settings.TILE_SIZE))
        self.image.fill(settings.COLOR["BOG"])

        self.rect = self.image.get_rect()
        self.rect.x = x * settings.TILE_SIZE
        self.rect.y = y * settings.TILE_SIZE

class Mountain(sprite.Sprite):
    def __init__(self, gamemap, x, y):
        self.groups = gamemap.sprite_group_all
        sprite.Sprite.__init__(self, self.groups)
        self.gamemap = gamemap
        self.x = x
        self.y = y

        self.image = Surface((settings.TILE_SIZE, settings.TILE_SIZE))
        self.image.fill(settings.COLOR["MOUNTAIN"])

        self.rect = self.image.get_rect()
        self.rect.x = x * settings.TILE_SIZE
        self.rect.y = y * settings.TILE_SIZE