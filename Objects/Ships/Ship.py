from Objects.GameObject import GameObject
from Utils.Orientation import Orientation


class Ship(GameObject):
    """
    Basisklasse für Schiffe mit gemeinsamer Logik für Treffer, Zerstörung und Bilddarstellung.

    Attribute:
        image_horizontal: Ressourcenpfad/Objekt für horizontale Darstellung.
        image_vertical: Ressourcenpfad/Objekt für vertikale Darstellung.
        hits (int): Anzahl registrierter Treffer.
    """
    def __init__(self, name: str, size: int, orientation: Orientation, image_horizontal, image_vertical,
                 coordinates: list[tuple[int, int]] = None):
        super().__init__(name, size, orientation, coordinates)
        self.image_horizontal = image_horizontal
        self.image_vertical = image_vertical
        self.hits = 0

    @property
    def image(self):
        return (
            self.image_horizontal if self.orientation == Orientation.HORIZONTAL
            else self.image_vertical
        )

    def on_hit(self, x, y):
        if self.hits < self.size:
            self.hits = self.hits + 1
        return self.is_destroyed

    @property
    def is_destroyed(self):
        return self.hits >= self.size
