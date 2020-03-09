from enum import Enum, auto
from random import randint

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
        # log("At loop " + str(entity.gm.GetLoop()) + ", " + entity.name +
        #     " recieved message from " + str(entity.gm.GetEntityName(telegram.senderID)) +
        #     " with message: " + str(telegram.msg) + ". Dispatch time: " +
        #      str(telegram.dispatchTime))

class StateProduced(State):
    def enter(self, entity):
        print("Beginning production of " +str(entity))
        self.accumulated_production = 0

    def execute(self, entity):
        self.accumulated_production += time.delta_time
        if self.accumulated_production >= entity.production_time:
            print("Completed production of " +str(entity))
            entity.spawn()

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

    def execute(self, entity):
        if self.stage is self.Stage.Done:
            if not self.finding_path and entity.owner.target_resource:
                self.finding_path = True
                goal = entity.owner.get_resource_location(entity.owner.target_resource)
                find_path(entity, entity.location, goal, self.__get_resource_path_callback)

        elif self.stage is self.Stage.Traversing:
            pass
            # go to resource
            # > Gathering

        elif self.stage is self.Stage.Gathering:
            if not self.finding_path: # and completed gathering
                self.finding_path = True
                goal = entity.owner.start_position
                find_path(entity, entity.location, goal, self.__get_delivery_path_callback)
            # tick progress
            # deduct one resource from tile
            # set carrying resource
            # > Delivering

        elif self.stage is self.Stage.Delivering:
            pass
            # get back to base

            # > Done

    def exit(self, entity):
        pass

    def on_message(self, entity, message):
        if message.msg == dispatcher.MSG.ArrivedAtGoal:
            if self.stage is self.Stage.Traversing:
                self.stage = self.Stage.Gathering
                # occupy one resource at tile
            elif self.stage is self.Stage.Delivering:
                # increment at base
                # remove resource from self
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
            find_path(entity, loc, goal, self.__get_path_callback)

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
def find_path(entity, location, goal, __callback):
        thread = c_thread.BaseThread(
            target=entity.gamemap.get_path,
            target_args=(location, goal),
            callback=__callback,
            callback_args=[entity]
        )
        thread.start()

