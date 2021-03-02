from GOAP2.__manager import __Manager

class SensorManager(__Manager):

    def __init__(self) -> None:
        super().__init__()
        self.working_memory = None
        self.sensors = []
        #self.update_interval = 1

    def set_working_memory(self, target):
        self.working_memory = target

    def add_sensor(self, sensor):
        sensor.set_working_memory(self.working_memory)
        self.sensors.append(sensor)

    def has_sensor(self, target):
        for s in self.sensors:
            if type(s).__name__ == target:
                return True
        return False

    def _update(self):
        # update sensors
        for sensor in self.sensors:
            sensor.update()