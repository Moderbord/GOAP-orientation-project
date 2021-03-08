import game_time as time

class __Manager():

    def __init__(self, agent_id: int) -> None:
        self.agent_id = agent_id
        self.update_interval = 0
        self.time_since_last_update = 0

    def setup(self):
        self.time_since_last_update = 0

    def update(self):
        self.time_since_last_update += time.clock.delta
        if self.time_since_last_update >= self.update_interval:
            self.time_since_last_update = 0
            self._update()

    # updated in inheritance
    def _update(self):
        pass
