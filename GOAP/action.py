import GOAP.action_set as action_set

class GOAPAction:

    def __init__(self):
        self.preconditions = action_set.ActionSet()
        self.effects = action_set.ActionSet()

        self.target = None
        self.minimun_range = 0
        self.in_range = False
        self.cost = 1.0

    def reset(self):
        self.in_range = False
        self.target = None

    def requires_in_range(self):
        pass

    def completed(self):
        pass

    def check_precondition(self, agent):
        pass

    def perform(self, agent):
        pass

    def is_in_range(self):
        return self.in_range

    def set_in_range(self, value):
        self.in_range = value

    def add_precondition(self, key, value):
        self.preconditions.add(key, value)

    def remove_precondition(self, key):
        for k in self.preconditions.keys():
            if key == k:
                self.preconditions[key] = None
                break

    def add_effect(self, key, value):
        self.effects.add(key, value)

    def remove_effect(self, key):
        for k in self.effects.keys():
            if key == k:
                self.effects[key] = None
                break


    
