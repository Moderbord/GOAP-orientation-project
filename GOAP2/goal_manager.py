from GOAP2.__manager import __Manager

class GoalManager(__Manager):

    def __init__(self) -> None:
        super().__init__()
        self.update_interval = 1
        self.current_goal = None
        self.goal_set = {}

    def _update(self):
        # update current goal
        pass

    def update_goal_revelancies(self):
        for goal in self.goal_set.values():
            self.goal_set[goal] = goal.update_relevance()

    def set_goal_set(self, goal_set):
        self.goal_set = goal_set

    def find_most_relevant_goal(self):
        return max(self.goal_set, key=self.goal_set.get)