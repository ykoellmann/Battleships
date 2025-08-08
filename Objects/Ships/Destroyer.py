from Objects.Ships.Ship import Ship
from Objects.Utils.Orientation import Orientation


class Destroyer(Ship):
    def __init__(self, orientation: Orientation, coordinates: list[tuple[int, int]] = None):
        image_horizontal = "path/to/destroyer_h.png"
        image_vertical = "path/to/destroyer_v.png"
        super().__init__("Destroyer", 3, orientation, image_horizontal, image_vertical, coordinates)