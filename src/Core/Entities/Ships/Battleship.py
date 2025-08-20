from src.Core.Entities.Ships.Ship import Ship
from src.Utils.Enums.Orientation import Orientation


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
        super().__init__("Battleship", 5, orientation, coordinates)
