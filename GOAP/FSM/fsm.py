
class FSM:

    def __init__(self):
        self.current_state = None

    def update(self):
        self.current_state()

    def set_state(self, state):
        self.current_state = state
