import game_time as time

class __Sensor():

    def __init__(self) -> None:
        self.update_interval = 0
        self.time_since_last_update = 0
        self.blackboard = None
        self.working_memory = None
        # set enabled?

    def setup(self):
        self.time_since_last_update = 0

    def set_blackboard(self, blackboard):
        self.blackboard = blackboard

    def set_working_memory(self, target):
        self.working_memory = target

    def update(self):
        self.time_since_last_update += time.clock.delta
        if self.time_since_last_update > self.update_interval:
            self.time_since_last_update = 0
            self._update()

    # updated in inheritance
    def _update(self):
        pass
