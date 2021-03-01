from GOAP2.__manager import __Manager

class TargetManager(__Manager):

    def __init__(self) -> None:
        super().__init__()
        self.update_interval = 1
        self.working_memory = None

    def select_best_target(self):
        pass

    def set_working_memory(self, target):
        self.working_memory = target

    def _update(self):
        pass