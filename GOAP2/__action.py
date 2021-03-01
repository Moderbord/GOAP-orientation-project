
class __Action():

    def __init__(self) -> None:
        self.preconditions = {}
        self.effects = {}
        self.interruptable = False
        self.cost = 0

    def validate_action(self):
        pass

    def apply_context_effects(self):
        pass

    def validate_context_preconditions(self):
        pass

    def activate_action(self):
        pass

    def is_action_complete(self):
        pass

    def get_cost(self):
        pass

