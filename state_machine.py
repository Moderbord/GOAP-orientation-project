class StateMachine:

    def __init__(self, owner):
        self.owner = owner
        self.currentState = None
        self.previousState = None
        self.globalState = None

    def Update(self):
        if(self.globalState):
            self.globalState.Execute(self.owner)

        if(self.currentState):
            self.currentState.Execute(self.owner)
        
    def ChangeState(self, newState):
        if(self.currentState and newState):
            #log(str(type(self.owner)) + " transition from " + str(type(self.currentState)) + " to " + str(type(newState)))
            self.previousState = self.currentState
            self.currentState.Exit(self.owner)
            self.currentState = newState
            self.currentState.Enter(self.owner)

    def EnterStateBlip(self, stateBlip):
        if(self.currentState and stateBlip):
            #log(str(type(self.owner)) + " transition from " + str(type(self.currentState)) + " to " + str(type(stateBlip)))
            self.previousState = self.currentState
            self.currentState = stateBlip
            self.currentState.Enter(self.owner)

    def RevertToPriorState(self):
        if(self.currentState and self.previousState):
            #log(str(type(self.owner)) + " reverting from " + str(type(self.currentState)) + " to " + str(type(self.previousState)))
            self.currentState.Exit(self.owner)
            self.currentState = self.previousState

    def IsInState(self, state):
        return self.currentState == state

    def HandleMessage(self, message):
        if(self.currentState and self.currentState.OnMessage(self.owner, message)):
            return True
        
        if(self.globalState and self.globalState.OnMessage(self.owner, message)):
            return True
        
        return False