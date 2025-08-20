from src.Core.Entities.Ships.Ship import Ship
from src.Utils.Orientation import Orientation


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
        image_horizontal = "path/to/submarine_h.png"
        image_vertical = "path/to/submarine_v.png"
        super().__init__("Submarine", 2, orientation, image_horizontal, image_vertical, coordinates)