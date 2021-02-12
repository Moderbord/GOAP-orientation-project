import queue

import game_time as time

from GOAP.FSM.fsm import FSM
from GOAP.planner import GOAPPlanner
from GOAP.transform import Position
from GOAP.transform import distance

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

        self.position = Position()  # put movement into other class?
        self.move_speed = 1         #
        self.move_progress = 0.0    #
        self.move_threshold = 1.0   #

    def start(self):
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

        # Moves agent until target arrives at destination
        if self.data_provider.move_agent(action):
            self.state_machine.set_state(self.perform_state)

    def perform_state(self):

        action = self.current_actions[0]
        if action.completed():
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

    def move_agent(self, next_action):
        if distance(self.position, next_action.target) <= next_action.minimun_range:
            next_action.set_in_range(True)
            return True
        
        if self.move_progress >= self.move_threshold:
            self.move_progress = 0
            # Move towards next action location
            if not self.position.x == next_action.target.x:
                self.position.x += self.move_speed if self.position.x < next_action.target.x else -self.move_speed

            if not self.position.y == next_action.target.y:
                self.position.y += self.move_speed if self.position.y < next_action.target.y else -self.move_speed

            #print(type(self).__name__ + " moving to [" + str(self.position.x) + ", " + str(self.position.y) + "]...")
            return False
        
        self.move_progress += time.clock.delta