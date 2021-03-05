class PriorityQueue:
    def __init__(self):
        self.elements = {}

    def empty(self):
        return len(self.elements) < 1

    def put(self, item, priority):
        self.elements[item] = priority

    def get(self):
        best_item, best_priority = None, 99999 # "infinity"
        for item, priority in self.elements.items():
            # Searches for the item with best priority
            if best_item is None or priority < best_priority:
                best_item, best_priority = item, priority
        
        # Pop and return from queue
        del self.elements[best_item]
        return best_item

class GOAPNode:

    def __init__(self, parent, cost, action, goal_state, world_state, action_set):
        self.parent = parent
        self.cost = cost
        self.action = action
        self.goal_state = goal_state
        self.world_state = world_state
        self.action_set = action_set

class GOAPPlanner():

    def build_plan(self, goal_state, world_state, action_set):
        
        start = GOAPNode(None, 0, None, goal_state, world_state, action_set)
        end = None

        queue = PriorityQueue()
        queue.put(start, 0)

        action_cost_table = {}

        while not queue.empty():
            # Get the current best option
            current = queue.get()

            # goal state can be fulfiled
            if self.solves_conditions(current.goal_state, current.world_state):
                end = current
                break

            unsatisfied_conditions = {key : value for key, value in current.goal_state.items() if current.goal_state[key] != current.world_state.get(key)}
            # Check cost of each available action that solves preconditions
            for action in self.available_actions(unsatisfied_conditions, current.action_set):
                # new cost is equal to current planning cost + targeted actions cost
                new_cost = current.cost + action.cost
                # If planning cost to action hasn't already been evaluated, or is lower than previous evaluated planning cost, update
                if action not in action_cost_table or new_cost < action_cost_table[action]:
                    action_cost_table[action] = new_cost
                    
                    new_goal_state = self.apply_action_context(current.goal_state, action.preconditions)
                    new_world_state = self.apply_action_context(current.world_state, action.effects)
                    action_subset = self.create_action_subset(current.action_set, action) # make a copy of current actions and remove self to stop recurrency

                    node = GOAPNode(current, new_cost, action, new_goal_state, new_world_state, action_subset)
                    queue.put(node, new_cost)

        # plan failed                    
        if end is None:
            return
        # create sequence
        action_sequence = []
        s = ""
        while True:
            if end.action is None:
                print(s + str(end.goal_state))
                break
            s += type(end.action).__name__ +" -> "
            action_sequence.append(end.action)
            end = end.parent

        return action_sequence

    def available_actions(self, goal_state, actions):
        _actions = [action for action in actions if self.solves_conditions(goal_state, action.effects)]
        return _actions

    def solves_conditions(self, conditions, state_values):
        for key, condition in conditions.items():
            current_condition = state_values.get(key)

            if current_condition is None: # values must exist..
                return False

            if current_condition is not condition: #..and solve conditions..
                return False

        return True

    def apply_action_context(self, current_state, action_context):
        new_state = {}
        new_state.update(current_state)
        new_state.update(action_context)
        return new_state

    def create_action_subset(self, actions, target):
        subset = actions.copy()
        subset.remove(target)
        return subset

g_planner = GOAPPlanner()