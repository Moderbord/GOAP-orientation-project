from GOAP2.blackboard import Blackboard
from enum import Enum, auto

import custom_thread as c_thread
import game_time as time
from game_server import g_map

from GOAP.transform import Position
from GOAP2.__manager import __Manager

class NavStatus(Enum):
    Invalid = auto()
    Pending = auto()
    Traversing = auto()
    Arrived = auto()

class NavigationManager(__Manager):

    def __init__(self) -> None:
        super().__init__()
        self.update_interval = 0 # currently depens on delta time every frame
        self.current_destination = None
        self.current_path = None
        # 
        self.next_tile = None
        self.move_threshold = 1
        self.move_progress = 0
        #

    def set_path(self, path):
        self.current_path = path
        position = self.blackboard.get_position()
        self.next_tile = self.current_path[position.tuple()]
        print("Found path")

    def move_to_next_position(self):
        new_position = Position(self.next_tile[0], self.next_tile[1])
        self.blackboard.set_position(new_position)
        # update next tile
        self.next_tile = self.current_path[self.next_tile]

    def _update(self):
        target = self.blackboard.get_navigation_target()
        # early out
        if target is None:
            self.blackboard.set_navigation_status(NavStatus.Invalid)
            return
            
        # check if target has updated and not currently has a pending find_path request
        if self.current_destination != target and not self.blackboard.has_navigation_status(NavStatus.Pending):
            self.current_destination = target
            self.current_path = None

            position = self.blackboard.get_position()
            self.blackboard.set_navigation_status(NavStatus.Pending)
            print("Destination changed! Looking for path to " + str(target.x) + "," + str(target.y))
            self.__find_path(position.tuple(), target.tuple(), self.__get_path_callback)

        if self.current_path:
            if self.next_tile is None:
                # Arrived
                self.current_path = None
                #self.current_destination = None
                self.blackboard.set_navigation_target(None)
                self.blackboard.set_navigation_status(NavStatus.Arrived)
                print("Arrived at destination")
                return True
            
            else:
                self.move_progress += time.clock.delta #* self.move_factor
                if self.move_progress >= self.move_threshold:
                    # reset progress
                    self.move_progress = 0
                    # move
                    self.move_to_next_position()
                self.blackboard.set_navigation_status(NavStatus.Traversing)

    # Method will create a separate thread and calculate a path between two points
    def __find_path(self, start, goal, __callback, fog=True):
            fog_filter_funtion = None
            # if Astar should find path through fog, pass it a function to do so
            # if fog:
            #     fog_filter_funtion = self.owner.gamemap.location_is_discovered

            thread = c_thread.BaseThread(
                target=g_map.get_path,
                target_args=(start, goal, fog_filter_funtion),
                callback=__callback,
                callback_args=[]
            )
            thread.start()

    def __get_path_callback(self, result):
        #self.finding_path = False
        if result:
            self.set_path(result)
        else:
            print("path callback result failed")