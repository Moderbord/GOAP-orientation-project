import queue
import GOAP.action_set as action_set

class GOAPNode:

    def __init__(self, parent, cost, state, action):
        self.parent = parent
        self.cost = cost
        self.state = action_set.ActionSet()
        self.action = action

    def __iter__(self):
        return self.cost

class GOAPPlanner:

    def __init__(self):
        self.usable_actions = []

    def plan(self, agent, available_actions, world_state=None, goal=None):

        for action in available_actions:
            # reset action?
            action.reset()

            # check available actions
            if action.check_precondition(agent):
                self.usable_actions.append(action)

        leaves = []
        start = GOAPNode(None, 0, world_state, None)

        success = self.build_graph(start, leaves, available_actions, goal)

        if not success:
            print("No plan!")
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
                result.append(cheapest_node.action)
                cheapest_node = cheapest_node.parent
            else:
                cheapest_node = None

        return result

    def build_graph(self, parent, leaves, usable_actions, goal):

        solution = False

        for action in usable_actions:
            if self.solves_conditions(action.preconditions, parent.state):

                current_state = self.populate_state(parent.state, action.effects)
                node = GOAPNode(parent, parent.cost + action.cost, current_state, action)

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
            if not state_conditions.get(k) == v:
                match = False

        return match

    def populate_state(self, parent_state, action_effects):
        new_state = action_set.ActionSet()
        new_state.update(parent_state)
        new_state.update(action_effects)

        return new_state
