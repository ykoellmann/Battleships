from Objects.GameObject import GameObject
from Objects.Utils.Orientation import Orientation


class Mine(GameObject):


    def __init__(self, coordinate: tuple[int, int] = None):
        super().__init__("Mine", 1, Orientation.HORIZONTAL, [coordinate])
        self.triggered = False

    def on_hit(self, x, y):
        self.triggered = True
        return self.is_destroyed

    def is_destroyed(self):
        return self.triggered

    @property
    def image(self):
        return self.image