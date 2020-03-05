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