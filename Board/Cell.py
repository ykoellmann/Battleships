from enum import Enum
from Objects.GameObject import GameObject
from Objects.Mine import Mine
from Objects.Ships.Ship import Ship


class CellState(Enum):
    """Darstellungszustand einer Zelle für die UI.

    Werte (Priorität der Anzeige):
        HIT_SHIP: Getroffene Schiffszelle (rot)
        HIT_MINE: Getroffene Mine (💣 auf schwarz)
        MISS:     Fehlschuss (schwarz)
        SHIP:     Ungeschlagene, belegte Schiffszelle (grau)
        EMPTY:    Leere Zelle (weiß)
    """
    EMPTY = 0
    SHIP = 1
    HIT_SHIP = 2
    MISS = 3
    HIT_MINE = 4
    MINE = 5


class Cell:
    """
    Repräsentiert eine einzelne Zelle des Spielfelds.

    Attribute:
        x (int): X-Koordinate der Zelle (Spalte).
        y (int): Y-Koordinate der Zelle (Zeile).
        object (GameObject | None): Belegendes Objekt (Schiff/Mine) oder None.
        is_shot (bool): Wurde bereits auf diese Zelle geschossen.
        is_adjacent (bool): Temporäre Markierung für angrenzende Felder (z. B. Hover-Vorschau).
    """
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.object: GameObject | None = None  # Objekt, das diese Zelle belegt
        self.is_shot: bool = False             # Wurde auf diese Zelle geschossen?
        self.is_adjacent: bool = False         # Wird als angrenzend angezeigt (z. B. Hover-Vorschau)

    def place_object(self, obj: GameObject):
        self.object = obj
        obj.is_placed = True

    def mark_adjacent(self):
        self.is_adjacent = True

    def clear_adjacent(self):
        self.is_adjacent = False

    def shoot(self) -> tuple[bool, bool, GameObject | None]:
        self.is_shot = True
        if self.object:
            return True, self.object.on_hit(self.x, self.y), self.object  # Treffer
        return False, False, None  # Fehlschuss

    @property
    def is_occupied(self) -> bool:
        return self.object is not None

    @property
    def is_hit(self) -> bool:
        """
        Prüft ob die Zelle getroffen wurde und ein Objekt enthält.

        Returns:
            bool: True wenn die Zelle getroffen wurde und ein Objekt enthält, sonst False
        """
        return self.is_shot and self.object is not None

    @property
    def is_miss(self) -> bool:
        return self.is_shot and self.object is None

    @property
    def has_ship(self) -> bool:
        return self.object is not None and isinstance(self.object, Ship)

    @property
    def has_mine(self) -> bool:
        return self.object is not None and isinstance(self.object, Mine)

    @property
    def state(self) -> CellState:
        """Ermittelt den UI-relevanten Zustand dieser Zelle.

        Die Priorität entspricht der bisherigen Anzeige-Logik:
        - Zuerst Trefferfälle unterscheiden (Schiff > Mine),
        - dann Fehlschuss,
        - dann sichtbares Schiff,
        - sonst leer.

        Returns:
            CellState: Aufbereiteter Darstellungszustand für die UI.
        """
        if self.is_hit and self.has_ship:
            return CellState.HIT_SHIP
        if self.is_hit and self.has_mine:
            return CellState.HIT_MINE
        if self.is_miss:
            return CellState.MISS
        if self.has_ship:
            return CellState.SHIP
        if self.has_mine:
            return CellState.MINE
        return CellState.EMPTY

