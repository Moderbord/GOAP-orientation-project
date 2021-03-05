from GOAP2.goap_planner import g_planner

class __Goal():

    def __init__(self) -> None:
        self.relevancy = 0.0
        self.goal_state = {}

    def get_relevancy(self):
        pass

    def clear_relevance(self):
        pass

    def apply_goal_state(self, state): # already in planner?
        state.update(self.goal_state)

    



