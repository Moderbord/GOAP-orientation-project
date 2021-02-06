class GOAPProvidable:

    def get_world_state(self):
        pass

    def create_goal_state(self):
        pass

    def plan_failed(self, failed_goal):
        pass

    def plan_found(self, goal, actions):
        pass

    def actions_finished(self):
        pass

    def plan_aborted(self, aborted_action):
        pass

    def move_agent(self, next_action):
        pass