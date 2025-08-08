from Objects.GameObject import GameObject
from Objects.Utils.Orientation import Orientation


class Ship(GameObject):
    def __init__(self, name: str, size: int, orientation: Orientation, image_horizontal, image_vertical,
                 coordinates: list[tuple[int, int]] = None):
        super().__init__(name, size, orientation, coordinates)
        self.image_horizontal = image_horizontal
        self.image_vertical = image_vertical

    @property.getter
    def image(self):
        return (
            self.image_horizontal if self.orientation == Orientation.HORIZONTAL
            else self.image_vertical
        )

    def on_hit(self, x, y):
        self.hits += 1
        return self.is_destroyed

    def is_destroyed(self):
        return self.hits >= self.size
