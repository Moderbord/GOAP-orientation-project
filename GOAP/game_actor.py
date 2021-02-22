from pygame.sprite import Sprite

import game_time as time
from game_settings import g_vars

from GOAP.transform import Position
from GOAP.transform import distance

class GameActor(Sprite):

    def __init__(self) -> None:
        self.position = Position()
        self.move_speed = 1
        self.move_progress = 0.0
        self.move_threshold = 1.0

        # sprite
        self.is_visible = False
        self.tile_size = g_vars["Game"]["TileSize"]
        
        self.image.fill(g_vars["Game"]["Colors"][self.tile_color])
        self.rect = self.image.get_rect()

    def start_actor(self):
        Sprite.__init__(self, self.groups)
        self.is_visible = True
        self.update()

    def move_actor(self, next_action):
        if distance(self.position, next_action.target) <= next_action.minimun_range:
            next_action.set_in_range(True)
            return True
        
        if self.move_progress >= self.move_threshold:
            self.move_progress = 0
            # Move towards next action location
            if not self.position.x == next_action.target.x:
                self.position.x += self.move_speed if self.position.x < next_action.target.x else -self.move_speed

            if not self.position.y == next_action.target.y:
                self.position.y += self.move_speed if self.position.y < next_action.target.y else -self.move_speed

            #print(type(self).__name__ + " moving to [" + str(self.position.x) + ", " + str(self.position.y) + "]...")
            return False
        
        self.move_progress += time.clock.delta

    def update(self):
        self.rect.x = self.position.x * self.tile_size + self.tile_size / 3
        self.rect.y = self.position.y * self.tile_size + self.tile_size / 3

    def destroy(self):
        if self.owner:
            self.owner.remove_unit(self)
        Sprite.remove(self, self.groups)
        #print("Removed " + type(self).__name__)