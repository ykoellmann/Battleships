import abc
from abc import ABC

from src.Utils.Orientation import Orientation


class GameObject(ABC):
    """
    Abstract base class for all game objects (e.g., ships, mines).

    Provides common functionality for game objects that can be placed on the
    board, including positioning, orientation, and hit handling.

    Attributes:
        name: Display name of the object
        size: Size/length of the object in cells
        coordinates: List of occupied coordinates (x, y)
        is_placed: True if the object has been placed on the board
        orientation: Orientation (horizontal/vertical)
    """
    def __init__(self, name: str, size: int, orientation: Orientation = Orientation.HORIZONTAL, coordinates: list[tuple[int, int]] = None):
        """
        Initialize a game object.

        Args:
            name: Display name of the object
            size: Length/size in cells
            orientation: Initial orientation
            coordinates: Optional starting coordinates
        """
        self.name = name
        self.size = size
        self.coordinates = coordinates if coordinates else []
        self.is_placed = False
        self.orientation = orientation

    def set_position(self, start_x: int, start_y: int):
        """
        Calculate and set coordinates based on starting point and orientation.

        Args:
            start_x: Starting column (x)
            start_y: Starting row (y)
        """
        if self.orientation == Orientation.HORIZONTAL:
            self.coordinates = [(start_x + i, start_y) for i in range(self.size)]
        else:  # Orientation.VERTICAL
            self.coordinates = [(start_x, start_y + i) for i in range(self.size)]

    @abc.abstractmethod
    def on_hit(self, x, y):
        """
        Called when one of this object's cells is hit.

        Args:
            x: X coordinate of the hit
            y: Y coordinate of the hit

        Returns:
            Implementation-dependent value (e.g., whether destroyed), optional
        """
        pass

    @property
    @abc.abstractmethod
    def is_destroyed(self) -> bool:
        """
        Check if this game object is completely destroyed.

        Returns:
            bool: True if the object is destroyed, False otherwise
        """
        pass

    def rotate(self):
        """
        Rotate the object's orientation (horizontal ↔ vertical).
        """
        self.orientation = self.orientation.rotate()

    @property
    @abc.abstractmethod
    def image(self):
        """
        Get the visual representation/image of this game object.

        Returns:
            Implementation-dependent image representation
        """
        pass

    def __str__(self):
        return f"{self.name} ({self.size}) [{str(self.orientation)}]"