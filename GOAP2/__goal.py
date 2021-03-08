class __Goal():

    def __init__(self) -> None:
        self.relevancy = 0.0
        self.goal_state = {}

    def get_relevancy(self, agent_id: int):
        pass

    def clear_relevance(self):
        pass

    def apply_goal_state(self, state): # already in planner?
        state.update(self.goal_state)

    



