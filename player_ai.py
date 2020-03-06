import state_machine as fsm
import message_dispatcher as dispatch
import ai_state
import entity_state


class AI:
    def __init__(self, gamemap, start_position):
        self.gamemap = gamemap
        self.start_position = start_position
        self.fsm = fsm.StateMachine(self)
        self.fsm.globalState = ai_state.AIGlobalState()
        self.fsm.currentState = ai_state.AIStateIdle()
        self.dispatcher = dispatch.MessageDispatcher()
        self.entity_list = []

    def Add_Entity(self, entity):
        self.entity_list.append(entity(self))