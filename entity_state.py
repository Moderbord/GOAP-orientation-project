from random import randint
import message_dispatcher as dispatcher
import custom_thread as c_thread

class State:

    def Enter(self, entity):
        pass

    def Execute(self, entity):
        pass

    def Exit(self, entity):
        pass

    def OnMessage(self, entity, message):
        pass
        # log("At loop " + str(entity.gm.GetLoop()) + ", " + entity.name +
        #     " recieved message from " + str(entity.gm.GetEntityName(telegram.senderID)) +
        #     " with message: " + str(telegram.msg) + ". Dispatch time: " +
        #      str(telegram.dispatchTime))

class StateIdle(State):
    def Enter(self, entity):
        entity.is_idle = True

    def Execute(self, entity):
        pass

    def Exit(self, entity):
        entity.is_idle = False

    def OnMessage(self, entity, message):
        pass

class StateExplore(State):
    def Enter(self, entity):
        pass

    def Execute(self, entity):
        if not entity.is_traversing and not entity.is_finding_path:

            entity.is_finding_path = True
            loc = entity.location
            goal = (randint(0, entity.gamemap.map_width - 1), (randint(0, entity.gamemap.map_height - 1)))
            
            thread = c_thread.BaseThread(
                target=entity.gamemap.get_path,
                target_args=(loc, goal),
                callback=self.__get_path_callback,
                callback_args=[entity]
            )
            thread.start()

    def Exit(self, entity):
        entity.is_traversing = False

    def OnMessage(self, entity, message):
        if message.msg == dispatcher.MSG.ArrivedAtGoal:
            entity.is_traversing = False

    def __get_path_callback(self, entity, result):
        entity.is_finding_path = False
        if result:
            entity.set_path(result)
            entity.is_traversing = True