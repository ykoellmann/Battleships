from src.Core.Entities.GameObject import GameObject
from src.Utils.Orientation import Orientation


class Mine(GameObject):
    """
    Represents a mine game object that can be placed on the board.

    A mine is a single-cell object that gets triggered when hit and is
    immediately destroyed upon being triggered.
    """
    def __init__(self, coordinate: tuple[int, int] = None):
        """
        Initialize a mine object.

        Args:
            coordinate: Optional initial coordinate for the mine
        """
        super().__init__("Mine", 1, Orientation.HORIZONTAL, [coordinate])
        self.triggered = False

    def on_hit(self, x, y):
        """
        Handle being hit by triggering the mine.

        Args:
            x: X coordinate of the hit
            y: Y coordinate of the hit

        Returns:
            bool: True since mine is destroyed when triggered
        """
        self.triggered = True
        return self.is_destroyed

    @property
    def is_destroyed(self):
        """
        Check if the mine has been triggered and is destroyed.

        Returns:
            bool: True if the mine has been triggered, False otherwise
        """
        return self.triggered

    @property
    def image(self):
        """
        Get the visual representation of the mine.

        Returns:
            str: Unicode bomb symbol representing the mine
        """
        return "💣"