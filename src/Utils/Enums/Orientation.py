from enum import Enum


class Orientation(Enum):
    """
    Orientation of a game object.

    Values:
        HORIZONTAL: Horizontal orientation.
        VERTICAL: Vertical orientation.
    """
    HORIZONTAL = 0
    VERTICAL = 1

    def rotate(self) -> "Orientation":
        """
        Return the rotated orientation (horizontal ↔ vertical).

        Returns:
            Orientation: The opposite orientation (HORIZONTAL <-> VERTICAL).
        """
        return Orientation.VERTICAL if self is Orientation.HORIZONTAL else Orientation.HORIZONTAL

    def __str__(self):
        return "Horizontal" if self == Orientation.HORIZONTAL else "Vertikal"