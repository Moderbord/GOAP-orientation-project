from enum import Enum, auto

class MSG(Enum):
    NewWorkerUnit = auto()
    NewExplorerUnit = auto()
    NewArtisanUnit = auto()
    NewSoldierUnit = auto()

    DoneProduced = auto()

    ArrivedAtGoal = auto()

class Message:
    def __init__(self, sender, msg, extra_info=None):
        self.sender = sender
        self.msg = msg
        self.extra_info = extra_info


class MessageDispatcher:
    def __init__(self):
        pass

    def __Discharge(self, receiver, msg):
        receiver.fsm.handle_message(msg)

    def Dispatch(self, sender, receiver, msg, extra_info):
        message = Message(sender, msg, extra_info)
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
