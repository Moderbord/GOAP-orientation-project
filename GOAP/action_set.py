
class ActionSet(dict):

    def __init__(self):
        #super().__init__()
        self = dict()

    def add(self, key, value):
        self[key] = value
        