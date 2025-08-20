from src.Core.Entities.Ships.Ship import Ship
from src.Utils.Orientation import Orientation


class Destroyer(Ship):
    """
    Destroyer - a fast and agile warship.
    
    A destroyer occupies 3 cells and is commonly used in naval fleets.
    It requires 3 hits to be destroyed.
    """
    def __init__(self, orientation: Orientation, coordinates: list[tuple[int, int]] = None):
        """
        Initialize a destroyer.
        
        Args:
            orientation: Initial orientation (horizontal or vertical)
            coordinates: Optional starting coordinates
        """
        image_horizontal = "path/to/destroyer_h.png"
        image_vertical = "path/to/destroyer_v.png"
        super().__init__("Destroyer", 3, orientation, image_horizontal, image_vertical, coordinates)