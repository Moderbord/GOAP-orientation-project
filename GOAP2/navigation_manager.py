from GOAP2.__manager import __Manager

class NavigationManager(__Manager):

    def __init__(self) -> None:
        super().__init__()
        self.update_interval = 1
        self.current_destination = None
        self.current_path = None

    def set_destination(self):
        pass

    def set_path(self):
        pass

    def move_to_next_position(self):
        pass

    def __update(self):
        pass