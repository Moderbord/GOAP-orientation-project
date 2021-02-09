import time
from pygame import time as pygame_time

class Clock():

    def __init__(self):
        self.__clock = pygame_time.Clock()
        self.delta = 0.0
        self.elapsed = 0.0

    def update(self, fps=1, speed=1):
        self.delta = self.__clock.tick(fps) / 1000.0 * speed
        self.elapsed += self.delta

def now():
    return time.time_ns() / 1000000

clock = Clock()
