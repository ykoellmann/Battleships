from src.Core.Entities.GameObject import GameObject
from src.Utils.Enums.Orientation import Orientation


class Ship(GameObject):
    """
    Base class for ships with common logic for hits, destruction and image display.

    Attributes:
        image_horizontal: Resource path/object for horizontal display
        image_vertical: Resource path/object for vertical display
        hits: Number of registered hits on this ship
    """
    def __init__(self, name: str, size: int, orientation: Orientation,
                 coordinates: list[tuple[int, int]] = None):
        super().__init__(name, size, orientation, coordinates)
        self.hits = 0

    def on_hit(self, x, y):
        """
        Handle being hit by incrementing hit count.
        
        Args:
            x: X coordinate of the hit
            y: Y coordinate of the hit
            
        Returns:
            bool: True if ship is destroyed after this hit, False otherwise
        """
        if self.hits < self.size:
            self.hits = self.hits + 1
        return self.is_destroyed

    @property
    def is_destroyed(self):
        """
        Check if ship is completely destroyed.
        
        Returns:
            bool: True if hits equal or exceed ship size, False otherwise
        """
        return self.hits >= self.size

    def destroy(self):
        """
        Instantly destroy the ship by setting hits to maximum size.
        
        This method is used when a ship hits a mine and needs to be 
        immediately destroyed regardless of previous damage.
        """
        self.hits = self.size
