from src.Core.Entities.Ships.Ship import Ship
from src.Utils.Orientation import Orientation


class Cruiser(Ship):
    """
    Cruiser - a medium-sized warship.
    
    A cruiser occupies 4 cells and is the second-largest ship in the fleet.
    It requires 4 hits to be destroyed.
    """
    def __init__(self, orientation: Orientation, coordinates: list[tuple[int, int]] = None):
        """
        Initialize a cruiser.
        
        Args:
            orientation: Initial orientation (horizontal or vertical)
            coordinates: Optional starting coordinates
        """
        image_horizontal = "path/to/cruiser_h.png"
        image_vertical = "path/to/cruiser_v.png"
        super().__init__("Cruiser", 4, orientation, image_horizontal, image_vertical, coordinates)