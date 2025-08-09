from Objects.Ships.Ship import Ship
from Utils.Orientation import Orientation


class Submarine(Ship):
    def __init__(self, orientation: Orientation, coordinates: list[tuple[int, int]] = None):
        image_horizontal = "path/to/submarine_h.png"
        image_vertical = "path/to/submarine_v.png"
        super().__init__("Submarine", 2, orientation, image_horizontal, image_vertical, coordinates)