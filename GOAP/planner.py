import queue

import game_time as time

from GOAP.action_set import ActionSet

class GOAPNode:

    def __init__(self, parent, cost, state, action):
        self.parent = parent
        self.cost = cost
        self.state = state
        self.action = action

    def __iter__(self):
        return self.cost

class GOAPPlanner:

    def plan(self, agent, available_actions, world_state=None, goal=None):
        t1 = time.now()
        
        usable_actions = []

        for action in available_actions:
            # reset action?
            action.reset()

            # check available actions
            if action.check_precondition(agent):
                usable_actions.append(action)

        leaves = []
        start = GOAPNode(None, 0, world_state, None)

        success = self.build_graph(start, leaves, usable_actions, goal)

        if not success:
            # print("Failed to evaluate plan")
            return None

        #cheapest_node = min(leaves)
        cheapest_node = None
        for node in leaves:
            if not cheapest_node:
                cheapest_node = node
            else:
                cheapest_node = node if node.cost < cheapest_node.cost else cheapest_node

        result = queue.deque()
        while cheapest_node:
            if cheapest_node.action:
                result.appendleft(cheapest_node.action)
                cheapest_node = cheapest_node.parent
            else:
                cheapest_node = None

        t2 = time.now()
        print("planning time: " + str(t2 - t1) + " ms")

        return result

    def build_graph(self, parent, leaves, usable_actions, goal):

        solution = False

        for action in usable_actions:
            if self.solves_conditions(action.preconditions, parent.state):

                current_state = self.populate_state(parent.state, action.effects)
                node = GOAPNode(parent, parent.cost + action.get_cost(), current_state, action)

                if self.solves_conditions(goal, current_state):
                    leaves.append(node)
                    solution = True
                else:
                    subset = self.subset(usable_actions, action)
                    solution = self.build_graph(node, leaves, subset, goal)

        return solution


    def subset(self, usable_actions, remove_action):
        new_set = set()
        for action in usable_actions:
            if not action == remove_action:
                new_set.add(action)

        return new_set

    def solves_conditions(self, preconditions, state_conditions):

        match = True

        for k, v in preconditions.items():
            if not state_conditions.get(k) == v: # values must exist and solve condition
                match = False

        return match

    # def solves_state(self, goal, current_state):

    #     match = False

    #     for state_key, state_value in current_state.items():
    #         goal_value = goal.get(state_key, None)

    #         if goal_value is None: # value doesn't exist in goal -> doesn't effect goal state
    #             continue

    #         if state_value != goal_value: # value exist and differs from goal state -> stop
    #             match = False
    #             break
    #         else:
    #             match = True # at least one match must be same as in goal state

    #     return match

    def populate_state(self, parent_state, action_effects):
        new_state = ActionSet()
        new_state.update(parent_state)
        new_state.update(action_effects)

        return new_state
