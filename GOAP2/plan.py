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

    def is_valid(self, blackboard):
        return False if self.action_plan is None else self.current_action.is_valid(blackboard)

    def activate(self, blackboard):
        self.current_action.activate(blackboard)

    def advance(self, blackboard):
        if self.action_plan.empty():
            self.action_plan = None
            return False

        self.current_action = self.action_plan.get()
        self.current_action.activate(blackboard)
        return True

    def is_step_interruptable(self):
        return self.current_action.interruptable

    def is_step_complete(self, blackboard):
        return self.current_action.is_complete(blackboard)
