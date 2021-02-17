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
        
        action_cost_table = {}

        for action in available_actions:
            # reset action?
            action.reset()

            # check available actions
            if action.check_precondition(agent):
                action_cost_table[action] = action.get_cost(agent)

        leaves = []
        start = GOAPNode(None, 0, world_state, None)

        success = self.build_graph(start, leaves, action_cost_table, goal)

        if not success:
            # print("Failed to evaluate plan")
            return None

        # cheapest_node = None
        # for node in leaves:
        #     if not cheapest_node:
        #         cheapest_node = node
        #     else:
        #         cheapest_node = node if node.cost < cheapest_node.cost else cheapest_node
        cheapest_node = min(leaves, key=lambda x: x.cost)

        result = queue.deque()
        while cheapest_node:
            if cheapest_node.action:
                result.appendleft(cheapest_node.action)
                cheapest_node = cheapest_node.parent
            else:
                cheapest_node = None

        t2 = time.now()
        #print("planning time: " + str(t2 - t1) + " ms")

        return result

    def build_graph(self, parent, leaves, action_cost_table, goal):

        solution = False

        for action in action_cost_table.keys():
            if self.solves_conditions(action.preconditions, parent.state):

                # TODO append unlocked actions
                current_state = self.populate_state(parent.state, action.effects)
                node = GOAPNode(parent, parent.cost + action_cost_table[action], current_state, action)

                if self.solves_conditions(goal, current_state):
                    leaves.append(node)
                    solution = True
                else:
                    subset = self.subset(action_cost_table, action)
                    solution = self.build_graph(node, leaves, subset, goal)

        return solution


    def subset(self, action_cost_table, remove_action):
        new_set = {}
        for action, cost in action_cost_table.items():
            if action == remove_action:
                continue
            new_set[action] = cost

        return new_set

    def solves_conditions(self, preconditions, state_conditions):

        for key, req_value in preconditions.items():
            cur_value = state_conditions.get(key)

            if cur_value is None: # values must exist..
                return False

            if not req_value == cur_value: #..and solve conditions..
                return False

            # if current_set.amount - required_set.amount < 0: #..and have the required amount
            #     return False

        return True

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
        new_state.update(parent_state)      # update with current base values
        new_state.update(action_effects)    # update with new values

        # for key, new_set in action_effects.items():     # take changes into account
        #     prev_set = new_state.get(key)
        #     if not prev_set:                            # value_set doesn't exist -> simply add
        #         new_state[key] = new_set
        #     else:                                       # value_set exist -> update to new value and add amount
        #         new_state.add(key, new_set.value, new_set.amount + prev_set.amount)

        return new_state
