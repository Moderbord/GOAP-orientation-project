import collections

class Queue:
    def __init__(self):
        self.elements = collections.deque()

    def empty(self):
        return len(self.elements) == 0

    def put(self, x):
        self.elements.append(x)

    def get(self):
        return self.elements.popleft()

class Stack:
    def __init__(self):
        self.elements = collections.deque()

    def empty(self):
        return len(self.elements) == 0

    def put(self, x):
        self.elements.append(x)

    def get(self):
        return self.elements.pop()

class PriorityQueue:
    def __init__(self):
        self.elements = {}

    def empty(self):
        return len(self.elements) == 0

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

class WeightedGraph:
    def __init__(self, gamemap):
        self.gamemap = gamemap

    def in_bounds(self, neighbor):
        (x, y) = neighbor
        return 0 <= x < self.gamemap.map_width and 0 <= y < self.gamemap.map_width

    def passable(self, neighbor):
        return neighbor not in self.gamemap.unpassable_tiles

    def cutting_corner(self, current, neighbor):
        (x, y) = neighbor
        # movement from current to neighbor
        dx = neighbor[0] - current[0]
        dy = neighbor[1] - current[1]
        # optimization (movement is not diagonal and check can be skipped)
        if (dx * dy == 0):
            return True
        # possible blocking walls
        posible_walls = [(x-dx, y), (x, y-dy)]
        # If any of the neighbors is a wall return false
        return posible_walls[0] not in self.gamemap.unpassable_tiles and posible_walls[1] not in self.gamemap.unpassable_tiles

    def neighbors(self, current):
        (x, y) = current

        # 8x movement
        current_neighbors = [(x+1, y), (x, y-1), (x-1, y), (x, y+1), (x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)]

        current_neighbors = filter(self.in_bounds, current_neighbors)
        current_neighbors = filter(self.passable, current_neighbors)
        current_neighbors = filter(lambda neighbor: self.cutting_corner(current, neighbor), current_neighbors)
        return current_neighbors

    def cost(self, from_node, to_node):
        # movement from current to neighbor
        dx = to_node[0] - from_node[0]
        dy = to_node[1] - from_node[1]
        # If movement delta is 0 => movement is not diagonal
        return 1 if (dx * dy == 0) else 1.4

# Manhattan distance heuristic
def HeuristicManhattar(from_node, to_node):
    (x1, y1) = from_node
    (x2, y2) = to_node
    return abs(x2 - x1) + abs(y2 - y1)

def Astar(graph, start, goal):

    if start == goal or start in graph.gamemap.unpassable_tiles or goal in graph.gamemap.unpassable_tiles:
        return False

    front = PriorityQueue()
    front.put(start, 0)
    path = {}
    travel_costs = {}
    path[start] = None
    travel_costs[start] = 0

    while not front.empty():
        # Get the current best option
        current = front.get()

        # Goal found
        if (current == goal):
            break

        # Check cost of each neighbor next to current
        for neighbor in graph.neighbors(current):
            # new cost is equal to current travel cost + cost to travel to next neighbor
            new_cost = travel_costs[current] + graph.cost(current, neighbor)
            # If travel cost to neighbor hasn't already been evaluated, or is lower than previous evaluated travel cost, update the travel cost
            if neighbor not in travel_costs or new_cost < travel_costs[neighbor]:
                travel_costs[neighbor] = new_cost

                priority = new_cost + HeuristicManhattar(neighbor, goal) # Manhattan

                front.put(neighbor, priority)
                path[neighbor] = current

    # reconstruct path
    current = goal
    trace = {}
    while current != start:
        trace[current] = path.get(current, False)
        if not trace[current]:
            return False
        current = path[current]
    trace[start] = None
    return trace