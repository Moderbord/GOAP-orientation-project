class GOAPProvidable:

    def create_world_state(self):
        pass

    def create_goal_state(self):
        pass

    def get_goal_state(self):
        return self.goal_state

    def set_goal_state(self, state):
        self.goal_state = state

    def plan_failed(self, failed_goal):
        pass

    def plan_found(self, goal, actions):
        string = "(" + type(self).__name__ + ") Plan found: "
        tmp = actions.copy()
        while len(tmp) > 0:
            a = tmp.popleft()
            string += type(a).__name__
            string += " -> "
        print(string + str(goal))
        
    def actions_finished(self):
        print(type(self).__name__ + " done actions!")

    def plan_aborted(self, aborted_action):
        print("Aborted plan: " + type(aborted_action).__name__)
        pass

    def move_agent(self, next_action):
        pass