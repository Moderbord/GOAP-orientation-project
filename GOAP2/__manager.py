import game_time as time

class __Manager():

    def __init__(self) -> None:
        self.update_interval = 0
        self.time_since_last_update = 0
        self.last_update = 0

    def setup(self):
        self.time_since_last_update = time.now()

    def update(self):
        current_time = time.now()
        if current_time - self.time_since_last_update > self.update_interval:
            self.time_since_last_update = current_time
            self.__update()

    # updated in inheritance
    def __update(self):
        pass

