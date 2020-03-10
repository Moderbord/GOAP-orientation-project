from enum import Enum, auto
from random import randint

from game_settings import g_vars
import message_dispatcher as dispatcher
import game_time as time
import custom_thread as c_thread
import game_entities as entities

class State:

    def enter(self, entity):
        pass

    def execute(self, entity):
        pass

    def exit(self, entity):
        pass

    def on_message(self, entity, message):
        pass

class StateProduced(State):
    def enter(self, entity):
        self.accumulated_production = 0

    def execute(self, entity):
        self.accumulated_production += time.delta_time
        if self.accumulated_production >= entity.production_time:
            entity.production_spawn()

    def exit(self, entity):
        pass

    def on_message(self, entity, message):
        pass

class StateLocked(State):
    def enter(self, entity):
        pass

    def execute(self, entity):
        pass

    def exit(self, entity):
        pass

    def on_message(self, entity, message):
        pass

class StateIdle(State):
    def enter(self, entity):
        entity.is_idle = True

    def execute(self, entity):
        pass

    def exit(self, entity):
        entity.is_idle = False

    def on_message(self, entity, message):
        pass

class StateGather(State):

    class Stage(Enum):
        Done = auto()
        Traversing = auto()
        Gathering = auto()
        Delivering = auto()

    def enter(self, entity):
        self.stage = self.Stage.Done
        self.finding_path = False
        self.gather_progress = 0
        self.gather_completion = False

    def execute(self, entity):
        if self.stage is self.Stage.Done:
            if not self.finding_path and entity.owner.target_resource:
                self.finding_path = True
                goal = entity.owner.get_resource_location(entity.owner.target_resource[2]) # class
                find_path(entity, entity.location, goal, self.__get_resource_path_callback)

        elif self.stage is self.Stage.Traversing:
            pass

        elif self.stage is self.Stage.Gathering:
            # gathering is done but doesn't have a path
            if self.gather_completion and not self.finding_path:
                self.finding_path = True
                goal = entity.owner.start_position
                find_path(entity, entity.location, goal, self.__get_delivery_path_callback)
            # if gathering is completed
            elif self.gather_progress >= g_vars[entity.owner.target_resource[0]][entity.owner.target_resource[1]]["GatherTime"]:
                self.gather_completion = True
            # tick progress
            self.gather_progress += time.delta_time

        elif self.stage is self.Stage.Delivering:
            pass

    def exit(self, entity):
        pass

    def on_message(self, entity, message):
        if message.msg == dispatcher.MSG.ArrivedAtGoal:
            if self.stage is self.Stage.Traversing:
                # check if tile has wanted resource remaining
                tile = entity.gamemap.get_background_tile(entity.location)
                if tile.has_free_resource_type(entity.owner.target_resource[2]):
                    # occupy that resource and shange stage
                    tile.occupy_resource(entity.owner.target_resource[2])
                    self.stage = self.Stage.Gathering
                # else entity will find try to find another resource
                else:
                    self.stage = self.Stage.Done

            elif self.stage is self.Stage.Delivering:
                if entity.carried_resource: # TODO fix this!!
                    # increment at base
                    entity.owner.add_resource(entity.carried_resource)
                    # remove resource from self
                    entity.carried_resource = None
                self.stage = self.Stage.Done

            return True

        return False

    def __get_resource_path_callback(self, entity, result):
        self.finding_path = False
        if result:
            self.stage = self.Stage.Traversing
            entity.set_path(result)

    def __get_delivery_path_callback(self, entity, result):
        self.finding_path = False
        if result:
            # safe to reset progress when path has been found
            self.gather_progress = 0
            self.gather_completion = False
            # deduct one resource from tile and carry it
            tile = entity.gamemap.get_background_tile(entity.location)
            entity.carried_resource = tile.deduct_resource(entity.owner.target_resource[2])
            # change stage and transport resource
            self.stage = self.Stage.Delivering
            entity.set_path(result)

class StateExplore(State):

    class Stage(Enum):
        Traversing = auto()
        Done = auto()

    def enter(self, entity):
        self.stage = self.Stage.Done
        self.finding_path = False

    def execute(self, entity):
        if self.stage is self.Stage.Done and not self.finding_path:
            self.finding_path = True
            loc = entity.location
            goal = (randint(0, entity.gamemap.tile_width - 1), (randint(0, entity.gamemap.tile_height - 1)))
            find_path(entity, loc, goal, self.__get_path_callback, False)

    def exit(self, entity):
        pass

    def on_message(self, entity, message):
        if message.msg == dispatcher.MSG.ArrivedAtGoal:
            self.stage = self.Stage.Done
            return True

        return False

    def __get_path_callback(self, entity, result):
        self.finding_path = False
        if result:
            self.stage = self.Stage.Traversing
            entity.set_path(result)

# Method will create a separate thread and calculate a path between two points
def find_path(entity, location, goal, __callback, fog=True):
        fog_filter_funtion = None
        # if Astar should find path through fog, pass it a function to do so
        if fog:
            fog_filter_funtion = entity.owner.gamemap.location_is_discovered
        thread = c_thread.BaseThread(
            target=entity.gamemap.get_path,
            target_args=(location, goal, fog_filter_funtion),
            callback=__callback,
            callback_args=[entity]
        )
        thread.start()

