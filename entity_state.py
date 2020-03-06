from random import randint

class State:

    def Enter(self, entity):
        pass

    def Execute(self, entity):
        pass

    def Exit(self, entity):
        pass

    def OnMessage(self, entity, telegram):
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

    def OnMessage(self, entity, telegram):
        pass

class StateExplore(State):
    def Enter(self, entity):
        pass

    def Execute(self, entity):
        if not entity.is_exploring:
            # random location
            path = entity.gamemap.get_path(entity.location, (randint(0, entity.gamemap.map_width - 1), (randint(0, entity.gamemap.map_height - 1))))
            if path:
                entity.set_path(path)
                entity.is_exploring = True

    def Exit(self, entity):
        entity.is_exploring = False

    def OnMessage(self, entity, telegram):
        pass