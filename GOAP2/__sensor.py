import game_time as time

class __Sensor():

    def __init__(self) -> None:
        self.update_interval = 0
        self.time_since_last_update = 0
        # set enabled?

    def setup(self):
        self.time_since_last_update = 0

    def update(self, agent_id: int):
        self.time_since_last_update += time.clock.delta
        if self.time_since_last_update > self.update_interval:
            self.time_since_last_update = 0
            self._update(agent_id)

    # updated in inheritance
    def _update(self, agent_id: int):
        pass
