from src.Core.Entities.Ships.Ship import Ship
from src.Utils.Enums.Orientation import Orientation


class Submarine(Ship):
    """
    Submarine - the smallest vessel in the fleet.
    
    A submarine occupies 2 cells and is the most compact ship.
    It requires 2 hits to be destroyed.
    """
    def __init__(self, orientation: Orientation, coordinates: list[tuple[int, int]] = None):
        """
        Initialize a submarine.
        
        Args:
            orientation: Initial orientation (horizontal or vertical)
            coordinates: Optional starting coordinates
        """
        super().__init__("Submarine", 2, orientation, coordinates)