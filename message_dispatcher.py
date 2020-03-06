from enum import Enum, auto

class MSG(Enum):
    ArrivedAtGoal = auto()

class Message:
    def __init__(self, sender, msg, extraInfo=None):
        self.sender = sender
        self.msg = msg
        self.extraInfo = extraInfo


class MessageDispatcher:
    def __init__(self):
        pass

    def __Discharge(self, receiver, msg):
        receiver.fsm.HandleMessage(msg)
        
    def Dispatch(self, sender, receiver, msg, extraInfo):
        message = Message(sender, msg, extraInfo)
        self.__Discharge(receiver, message)
        
        # if(delay <= 0):
        #     self.__Discharge(receiver, telegram)
        # else:
        #     currentLoop = self.gm.GetLoop()
        #     telegram.dispatchTime = currentLoop + delay
        #     key = str(senderID) + str(msg) + str(receiverID)
        #     self.priorityQ[key] = telegram

    # def DispatchDelayedMessage(self):
    #     currentLoop = self.gm.GetLoop()
    #     # Loop through copy so main queue can change during loop
    #     copiedQ = copy(self.priorityQ)
        
    #     for telegram in copiedQ.values():
    #         if(telegram.dispatchTime == currentLoop):
    #             receiver = self.gm.GetEntity(telegram.receiverID)
    #             self.__Discharge(receiver, telegram)
