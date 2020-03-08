from random import randint
import message_dispatcher as dispatcher
import game_time as time
import custom_thread as c_thread

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
        self.accumulated_production = 0

    def execute(self, entity):
        self.accumulated_production += time.delta_time
        if self.accumulated_production >= entity.production_time:
            entity.spawn()
            entity.fsm.change_state(StateIdle())

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

class StateExplore(State):
    def enter(self, entity):
        pass

    def execute(self, entity):
        if not entity.is_traversing and not entity.is_finding_path:

            entity.is_finding_path = True
            loc = entity.location
            goal = (randint(0, entity.gamemap.tile_width - 1), (randint(0, entity.gamemap.tile_height - 1)))
            
            thread = c_thread.BaseThread(
                target=entity.gamemap.get_path,
                target_args=(loc, goal),
                callback=self.__get_path_callback,
                callback_args=[entity]
            )
            thread.start()

    def exit(self, entity):
        entity.is_traversing = False

    def on_message(self, entity, message):
        if message.msg == dispatcher.MSG.ArrivedAtGoal:
            entity.is_traversing = False
            return True

        return False

    def __get_path_callback(self, entity, result):
        entity.is_finding_path = False
        if result:
            entity.set_path(result)
            entity.is_traversing = True