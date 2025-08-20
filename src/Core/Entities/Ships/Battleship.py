from src.Core.Entities.Ships.Ship import Ship
from src.Utils.Orientation import Orientation


class Battleship(Ship):
    """
    Battleship - the largest ship in the fleet.
    
    A battleship occupies 5 cells and is the most valuable target.
    It requires 5 hits to be destroyed.
    """
    def __init__(self, orientation: Orientation, coordinates: list[tuple[int, int]] = None):
        """
        Initialize a battleship.
        
        Args:
            orientation: Initial orientation (horizontal or vertical)
            coordinates: Optional starting coordinates
        """
        image_horizontal = "path/to/battleship_h.png"  # Path or loaded image
        image_vertical = "path/to/battleship_v.png"
        super().__init__("Battleship", 5, orientation, image_horizontal, image_vertical, coordinates)
