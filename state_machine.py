class StateMachine:

    def __init__(self, owner):
        self.owner = owner
        self.currentState = None
        self.previousState = None
        self.globalState = None

    def update(self):
        if(self.globalState):
            self.globalState.execute(self.owner)

        if(self.currentState):
            self.currentState.execute(self.owner)
        
    def change_state(self, newState):
        if(self.currentState and newState):
            #log(str(type(self.owner)) + " transition from " + str(type(self.currentState)) + " to " + str(type(newState)))
            self.previousState = self.currentState
            self.currentState.exit(self.owner)
            self.currentState = newState
            self.currentState.enter(self.owner)

    def enter_state_blip(self, stateBlip):
        if(self.currentState and stateBlip):
            #log(str(type(self.owner)) + " transition from " + str(type(self.currentState)) + " to " + str(type(stateBlip)))
            self.previousState = self.currentState
            self.currentState = stateBlip
            self.currentState.enter(self.owner)

    def revert_to_prior_state(self):
        if(self.currentState and self.previousState):
            #log(str(type(self.owner)) + " reverting from " + str(type(self.currentState)) + " to " + str(type(self.previousState)))
            self.currentState.exit(self.owner)
            self.currentState = self.previousState

    def is_in_state(self, state):
        return self.currentState == state

    def handle_message(self, message):
        if(self.currentState and self.currentState.on_message(self.owner, message)):
            return True
        
        if(self.globalState and self.globalState.on_message(self.owner, message)):
            return True
        
        return False