from pygame.sprite import Sprite

import game_time as time
import custom_thread as c_thread
from game_settings import g_vars

from GOAP.transform import Position
from GOAP.transform import distance

class GameActor(Sprite):

    def __init__(self) -> None:
        self.position = Position(1, 1)
        self.move_speed = 1
        self.move_progress = 0.0
        self.move_threshold = 1.0

        # sprite
        self.is_visible = False
        self.tile_size = g_vars["Game"]["TileSize"]
        
        self.image.fill(g_vars["Game"]["Colors"][self.tile_color])
        self.rect = self.image.get_rect()

        # pathfinding
        self.finding_path = False
        self.current_path = None
        self.current_tile = None
        self.next_tile = None

    def start_actor(self):
        Sprite.__init__(self, self.groups)
        self.is_visible = True
        self.update()

    # Old movement
    # def move_actor(self, next_action):
    #     if distance(self.position, next_action.target) <= next_action.minimun_range:
    #         next_action.set_in_range(True)
    #         return True
        
    #     if self.move_progress >= self.move_threshold:
    #         self.move_progress = 0
    #         # Move towards next action location
    #         if not self.position.x == next_action.target.x:
    #             self.position.x += self.move_speed if self.position.x < next_action.target.x else -self.move_speed

    #         if not self.position.y == next_action.target.y:
    #             self.position.y += self.move_speed if self.position.y < next_action.target.y else -self.move_speed

    #         #print(type(self).__name__ + " moving to [" + str(self.position.x) + ", " + str(self.position.y) + "]...")
    #         return False
        
    #     self.move_progress += time.clock.delta

    def move(self, dx=0, dy=0):
        self.position = Position(self.position.x + dx, self.position.y + dy)
        self.current_tile = self.owner.game_map.get_background_tile((self.position.x, self.position.y))

    def move_actor(self, next_action):
        # movement
        if self.current_path:

            if self.next_tile is None:
                self.current_path = None
                # Arrived
                next_action.set_in_range(True)
                return True
            
            else:
                (x1, y1) = self.position.x, self.position.y # TODO not update this every frame 
                (x2, y2) = self.next_tile
                dx, dy = x2 - x1, y2 - y1
                # get required movement threshold
                self.move_threshold = self.current_tile.movement_straight if (dx * dy == 0) else self.current_tile.movement_diagonal
                # take movement factor into account
                self.move_progress += time.clock.delta #* self.move_factor
                if self.move_progress >= self.move_threshold:
                    # reset progress
                    self.move_progress = 0
                    # move
                    self.move(dx, dy)
                    # update next tile
                    self.next_tile = self.current_path[self.next_tile]
        
        else:
            if not self.finding_path:
                self.finding_path = True
                target_position = (next_action.target.x, next_action.target.y)
                self.find_path(target_position, self.get_path_callback)
        
        return False

    def update(self):
        self.rect.x = self.position.x * self.tile_size + self.tile_size / 3
        self.rect.y = self.position.y * self.tile_size + self.tile_size / 3

    def destroy(self):
        if self.owner:
            self.owner.remove_unit(self)
        Sprite.remove(self, self.groups)
        #print("Removed " + type(self).__name__)

    def set_path(self, path):
        position = (self.position.x, self.position.y)
        
        self.current_path = path
        self.current_tile = self.owner.game_map.get_background_tile(position)
        self.next_tile = path[position]

    # Method will create a separate thread and calculate a path between two points
    def find_path(self, goal, __callback, fog=True):
            fog_filter_funtion = None
            # if Astar should find path through fog, pass it a function to do so
            # if fog:
            #     fog_filter_funtion = self.owner.gamemap.location_is_discovered
            position = (self.position.x, self.position.y)
            thread = c_thread.BaseThread(
                target=self.owner.game_map.get_path,
                target_args=(position, goal, fog_filter_funtion),
                callback=__callback,
                callback_args=[]
            )
            thread.start()

    def get_path_callback(self, result):
        self.finding_path = False
        if result:
            self.set_path(result)
        else:
            print("path callback result failed")