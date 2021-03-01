from GOAP2.__manager import __Manager

class SensorManager(__Manager):

    def __init__(self) -> None:
        super().__init__()
        self.update_interval = 1

    def _update(self):
        # update sensors
        pass