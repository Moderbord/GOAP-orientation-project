
class Position:

    def __init__(self, pos_x=0, pos_y=0):
        self.x = pos_x
        self.y = pos_y

    def __eq__(self, o: object) -> bool:
        return False if o is None else self.x == o.x and self.y == o.y

    def set_position(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y

    def set_x(self, value):
        self.x = value

    def set_y(self, value):
        self.y = value

    def tuple(self):
        return (self.x, self.y)

def distance(pos1, pos2):
    return abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y)
