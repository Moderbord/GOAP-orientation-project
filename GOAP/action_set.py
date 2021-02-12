class SetValue():

    def __init__(self, value, amount):
        self.value = value
        self.amount = amount

class ActionSet(dict):

    def __init__(self):
        #super().__init__()
        self = dict()

    def add(self, key, value, amount=0):
        #self[key] = SetValue(value, amount)
        self[key] = value
        