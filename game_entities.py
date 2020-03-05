from pygame import sprite
from pygame import Surface

import game_settings as settings

class BasicGameEntity(sprite.Sprite):

    def __init__(self, gamemap, location):
        sprite.Sprite.__init__(self, self.groups)
        # reference to map
        self.gamemap = gamemap
        # list of requirements for production
        self.prerequisite = []
        self.production_time = 0
        self.location = location

        self.image = Surface((settings.TILE_SIZE, settings.TILE_SIZE))
        self.image.fill(settings.COLOR[self.tile_color])
        self.rect = self.image.get_rect()

class BasicGameUnit(BasicGameEntity):

    def __init__(self, gamemap, location):
        BasicGameEntity.__init__(self, gamemap, location)
        self.move_speed = 0
        self.move_progress = 0

        # pathfinding
        self.current_path = None
        self.next_tile = None

    def set_path(self, path):
        self.current_path = path
        self.next_tile = path[self.location]

    def move(self, dx=0, dy=0):
        new_pos = self.location[0] + dx, self.location[1] + dy
        self.location = new_pos

    def update(self):
        # movement
        if self.current_path:
            (x1, y1), (x2, y2) = self.location, self.next_tile
            dx, dy = x2 - x1, y2 - y1

            current_tile = self.gamemap.get_background_tile(self.location)

            self.move_progress += self.move_speed * current_tile.movement_factor
            if self.move_progress >= 100:
                # reset progress
                self.move_progress = 0
                # move
                self.move(dx, dy)
                # update next tile
                self.next_tile = self.current_path[self.next_tile]
            
            if self.next_tile is None:
                self.current_path = None

        # drawing
        self.rect.x = self.location[0] * settings.TILE_SIZE
        self.rect.y = self.location[1] * settings.TILE_SIZE

class TestExplorer(BasicGameUnit):
    def __init__(self, gamemap, location):
        self.groups = gamemap.sprite_group_entities
        self.tile_color = "RED"
        BasicGameUnit.__init__(self, gamemap, location)
        self.move_speed = 10

    def move(self, dx=0, dy=0):
        new_pos = self.location[0] + dx, self.location[1] + dy
        if new_pos in self.gamemap.unpassable_tiles:
            return
        self.location = new_pos
        
        if dx: # horizontal movement
            start = (new_pos[0] + dx, new_pos[1] - 1)
            stop = (new_pos[0] + dx, new_pos[1] + 1)
            self.gamemap.clear_fog_area(start, stop)
        if dy: # vertical movement
            start = (new_pos[0] - 1, new_pos[1] + dy)
            stop = (new_pos[0] + 1, new_pos[1] + dy)
            self.gamemap.clear_fog_area(start, stop)
