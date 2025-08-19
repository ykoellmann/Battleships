from src.Core.Entities.Ships.Ship import Ship
from src.Utils.Orientation import Orientation


class Cruiser(Ship):
    def __init__(self, orientation: Orientation, coordinates: list[tuple[int, int]] = None):
        image_horizontal = "path/to/cruiser_h.png"
        image_vertical = "path/to/cruiser_v.png"
        super().__init__("Cruiser", 4, orientation, image_horizontal, image_vertical, coordinates)