import queue

import custom_thread as c_thread

from GOAP.FSM.fsm import FSM
from GOAP.planner import GOAPPlanner


class GOAPAgent:

    def __init__(self):
        self.state_machine = FSM()

        self.__state_idle = None
        self.__state_move = None
        self.__state_perform = None

        self.available_actions = set()
        self.current_actions = queue.deque()
        
        self.owner = None
        self.data_provider = None
        self.planner = GOAPPlanner()

    def start_agent(self):
        self.__state_idle = self.idle_state
        self.__state_move = self.move_state
        self.__state_perform = self.perform_state
        self.state_machine.set_state(self.idle_state)

    def update(self):
        self.state_machine.update()

    def add_action(self, action):
        self.available_actions.add(action)

    def get_action(self, action):
        pass

    def remove_action(self, action):
        pass

    def has_action_plan(self):
        return len(self.current_actions) > 0

    def idle_state(self):
        world_state = self.data_provider.create_world_state()
        goal = self.data_provider.create_goal_state()

        plan = self.planner.plan(self, self.available_actions, world_state, goal)
        if plan:
            self.current_actions = plan
            self.data_provider.plan_found(goal, plan)
            self.state_machine.set_state(self.perform_state)

        else:
            self.data_provider.plan_failed(goal)
            self.state_machine.set_state(self.idle_state)

    def move_state(self):
        action = self.current_actions[0]

        if action.requires_in_range() and action.target is None:
            print("Action requires target!! Plan failed")
            self.state_machine.set_state(self.idle_state)
            return

        # Moves agent until target arrives at destination
        if self.data_provider.move_actor(action):
            self.state_machine.set_state(self.perform_state)

    def perform_state(self):

        action = self.current_actions[0]
        if not action.started:
            action.on_start(self)

        if action.completed():
            action.on_end(self)
            self.current_actions.popleft()
        
        if self.has_action_plan():
            action = self.current_actions[0]
            in_range = action.is_in_range() if action.requires_in_range() else True

            if in_range:
                success = action.perform(self)

                if not success:
                    self.state_machine.set_state(self.idle_state)
                    self.data_provider.plan_aborted(action)
            
            else:
                self.state_machine.set_state(self.move_state)        
        
        else:
            self.state_machine.set_state(self.idle_state)
            self.data_provider.actions_finished()

