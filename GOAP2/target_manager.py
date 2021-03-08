from GOAP2.__manager import __Manager
from GOAP2.working_memory import g_wmm
from GOAP2.blackboard import g_bbm

class TargetManager(__Manager):

    def __init__(self, agent_id) -> None:
        super().__init__(agent_id)
        self.update_interval = 1.2
        self.target_fact_type = None
        self.targeting_function = None

    def select_best_target(self):
        fact = None
        if self.targeting_function:
            fact = g_wmm.get_working_memory(self.agent_id).read_fact_type_where(self.target_fact_type, self.targeting_function)
        else:
            fact = g_wmm.get_working_memory(self.agent_id).get_fact_with_highest_confidence(self.target_fact_type, lambda x: x.position.confidence)

        blackboard = g_bbm.get_blackboard(self.agent_id)
        if fact:
            blackboard.set_navigation_target(fact.position.value)
            blackboard.set_target_fact_type(None)
        else:
            blackboard.set_navigation_target(None)
            #print("Didn't find any targeting fact")

    def _update(self):
        blackboard = g_bbm.get_blackboard(self.agent_id)
        if blackboard.has_manual_navigation():
            return

        self.target_fact_type = blackboard.get_target_fact_type()
        self.targeting_function = blackboard.get_targeting_function()
        if self.target_fact_type:
            self.select_best_target()