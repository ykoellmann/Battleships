from Objects.Ships.Ship import Ship
from Utils.Orientation import Orientation


class Battleship(Ship):
    def __init__(self, orientation: Orientation, coordinates: list[tuple[int, int]] = None):
        image_horizontal = "path/to/battleship_h.png"  # Pfad oder geladenes Image
        image_vertical = "path/to/battleship_v.png"
        super().__init__("Battleship", 5, orientation, image_horizontal, image_vertical, coordinates)
