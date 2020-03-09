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
    def enter(self, entity):
        pass

    def execute(self, entity):
        if not entity.is_traversing and not entity.is_finding_path and entity.owner.target_resource:

            entity.is_finding_path = True
            loc = entity.location
            goal = entity.owner.get_resource_location(entity.owner.target_resource)
            find_path(entity, loc, goal)

    def exit(self, entity):
        entity.is_traversing = False

    def on_message(self, entity, message):
        if message.msg == dispatcher.MSG.ArrivedAtGoal:
            entity.is_traversing = False
            return True

        return False

class StateExplore(State):
    def enter(self, entity):
        pass

    def execute(self, entity):
        if not entity.is_traversing and not entity.is_finding_path:

            entity.is_finding_path = True
            loc = entity.location
            goal = (randint(0, entity.gamemap.tile_width - 1), (randint(0, entity.gamemap.tile_height - 1)))
            find_path(entity, loc, goal)

    def exit(self, entity):
        entity.is_traversing = False

    def on_message(self, entity, message):
        if message.msg == dispatcher.MSG.ArrivedAtGoal:
            entity.is_traversing = False
            return True

        return False

def find_path(entity, location, goal):
        thread = c_thread.BaseThread(
            target=entity.gamemap.get_path,
            target_args=(location, goal),
            callback=__get_path_callback,
            callback_args=[entity]
        )
        thread.start()

def __get_path_callback(entity, result):
    entity.is_finding_path = False
    if result:
        entity.set_path(result)
        entity.is_traversing = True