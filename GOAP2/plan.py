from queue import Queue

class Plan():

    def __init__(self) -> None:
        self.action_plan = None
        self.current_action = None
        self.plan_length = None

    def set_action_plan(self, action_plan):
        self.action_plan = Queue()
        for plan in action_plan:
            self.action_plan.put(plan)
        self.current_action = self.action_plan.get()
        self.plan_length = len(action_plan)

    def is_valid(self, agent_id):
        return False if self.action_plan is None else self.current_action.is_valid(agent_id)

    def activate(self, agent_id):
        self.current_action.activate(agent_id)

    def advance(self, agent_id):
        if self.action_plan.empty():
            self.action_plan = None
            return False

        self.current_action = self.action_plan.get()
        self.current_action.activate(agent_id)
        return True

    def is_step_interruptable(self):
        return self.current_action.interruptable

    def is_step_complete(self, agent_id):
        return self.current_action.is_complete(agent_id)
