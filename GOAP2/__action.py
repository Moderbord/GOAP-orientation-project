
class __Action():

    def __init__(self) -> None:
        self.preconditions = {}
        self.effects = {}
        self.interruptable = False
        self.cost = 3

    def is_valid(self, blackboard):
        return True

    def apply_context_effects(self): # already in planner?
        pass

    def is_applicable(self, blackboard):
        pass

    def activate(self, blackboard):
        pass

    def is_complete(self, blackboard):
        pass

    def get_cost(self): # currently redundant
        return self.cost

