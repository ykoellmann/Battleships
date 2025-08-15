import abc
from abc import ABC

from Utils.Orientation import Orientation


class GameObject(ABC):
    """
    Abstrakte Basis-Klasse für alle Spielobjekte (z. B. Schiffe, Minen).

    Attribute:
        name (str): Anzeigename des Objekts.
        size (int): Größe/Länge des Objekts in Zellen.
        coordinates (list[tuple[int,int]]): Liste der belegten Koordinaten (x, y).
        is_placed (bool): True, wenn das Objekt auf dem Board platziert wurde.
        orientation (Orientation): Ausrichtung (horizontal/vertikal).
    """
    def __init__(self, name: str, size: int, orientation: Orientation = Orientation.HORIZONTAL, coordinates: list[tuple[int, int]] = None):
        """Initialisiert ein Spielobjekt.

        Args:
            name (str): Anzeigename des Objekts.
            size (int): Länge/Größe in Zellen.
            orientation (Orientation): Anfangsausrichtung.
            coordinates (list[tuple[int,int]] | None): Optionale Startkoordinaten.
        """
        self.name = name
        self.size = size
        self.coordinates = coordinates if coordinates else []
        self.is_placed = False
        self.orientation = orientation

    def set_position(self, start_x: int, start_y: int):
        """Berechnet und setzt die Koordinaten basierend auf Startpunkt und Ausrichtung.

        Args:
            start_x (int): Start-Spalte (x).
            start_y (int): Start-Zeile (y).
        """
        if self.orientation == Orientation.HORIZONTAL:
            self.coordinates = [(start_x + i, start_y) for i in range(self.size)]
        else:  # Orientation.VERTICAL
            self.coordinates = [(start_x, start_y + i) for i in range(self.size)]

    @abc.abstractmethod
    def on_hit(self, x, y):  # bei Treffer
        """Wird aufgerufen, wenn eine der Zellen dieses Objekts getroffen wurde.

        Args:
            x: X-Koordinate des Treffers.
            y: Y-Koordinate des Treffers.
        Returns:
            Beliebiger Wert je nach Implementierung (z. B. ob zerstört), optional.
        """
        pass

    @property
    @abc.abstractmethod
    def is_destroyed(self) -> bool:
        pass

    def rotate(self):
        """Dreht die Ausrichtung des Objekts (horizontal ↔ vertikal)."""
        self.orientation = self.orientation.rotate()

    @property
    @abc.abstractmethod
    def image(self):
        pass

    def __str__(self):
        return f"{self.name} ({self.size}) [{str(self.orientation)}]"