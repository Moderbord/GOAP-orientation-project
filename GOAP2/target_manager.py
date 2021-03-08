from GOAP2.__manager import __Manager
from GOAP2.working_memory import FactType

class TargetManager(__Manager):

    def __init__(self) -> None:
        super().__init__()
        self.update_interval = 1.2
        self.working_memory = None
        self.target_fact_type = None

    def select_best_target(self):
        fact = self.working_memory.get_fact_with_highest_confidence(self.target_fact_type, lambda attrib: attrib.position.confidence)
        if fact:
            self.blackboard.set_navigation_target(fact.position.value)
            self.blackboard.set_target_fact_type(None)
        else:
            self.blackboard.set_navigation_target(None)
            #print("Didn't find any targeting fact")

    def set_working_memory(self, target):
        self.working_memory = target

    def _update(self):
        self.target_fact_type = self.blackboard.get_target_fact_type()
        if self.target_fact_type is not None:
            self.select_best_target()