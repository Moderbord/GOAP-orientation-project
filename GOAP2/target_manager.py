from GOAP2.__manager import __Manager

class TargetManager(__Manager):

    def __init__(self) -> None:
        super().__init__()
        self.update_interval = 1

    def select_best_target(self):
        pass

    def __update(self):
        pass