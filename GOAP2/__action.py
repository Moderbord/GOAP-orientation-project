class __Action():

    def __init__(self) -> None:
        self.preconditions = {}
        self.effects = {}
        self.interruptable = False
        self.cost = 3

    def is_valid(self, agent_id: int):
        return True

    def apply_context_effects(self): # already in planner?
        pass

    def is_valid_in_context(self, agent_id: int):
        return True

    def activate(self, agent_id: int):
        pass

    def is_complete(self, agent_id: int):
        pass

    def get_cost(self, agent_id: int): # currently redundant
        return self.cost

