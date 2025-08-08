from Objects.GameObject import GameObject


class Mine(GameObject):


    def __init__(self, coordinate: tuple[int, int] = None):
        super().__init__("Mine", 1, [coordinate])
        self.triggered = False
        self.image = None

    def on_hit(self, x, y):
        self.triggered = True
        return self.is_destroyed

    def is_destroyed(self):
        return self.triggered

    @property
    def image(self):
        return self.image