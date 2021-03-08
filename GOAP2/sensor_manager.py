from GOAP2.__manager import __Manager

class SensorManager(__Manager):

    def __init__(self, agent_id) -> None:
        super().__init__(agent_id)
        self.sensors = []
        #self.update_interval = 1

    def add_sensor(self, sensor):
        self.sensors.append(sensor)

    def has_sensor(self, target):
        for s in self.sensors:
            if type(s).__name__ == target:
                return True
        return False

    def _update(self):
        # update sensors
        for sensor in self.sensors:
            sensor.update(self.agent_id)