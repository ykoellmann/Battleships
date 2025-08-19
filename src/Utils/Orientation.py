from enum import Enum


class Orientation(Enum):
    """
    Ausrichtung eines Spielobjekts.

    Werte:
        HORIZONTAL: Waagerechte Ausrichtung.
        VERTICAL: Senkrechte Ausrichtung.
    """
    HORIZONTAL = 0
    VERTICAL = 1

    def rotate(self) -> "Orientation":
        """Gibt die gedrehte Ausrichtung zurück (horizontal ↔ vertikal).

        Returns:
            Orientation: Die jeweils andere Ausrichtung (HORIZONTAL <-> VERTICAL).
        """
        return Orientation.VERTICAL if self is Orientation.HORIZONTAL else Orientation.HORIZONTAL

    def __str__(self):
        return "Horizontal" if self == Orientation.HORIZONTAL else "Vertikal"