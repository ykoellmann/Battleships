from enum import Enum
from src.Core.Entities.GameObject import GameObject
from src.Core.Entities.Mine import Mine
from src.Core.Entities.Ships.Ship import Ship
from src.Utils.Objects.ShootResult import ShootResult


class CellState(Enum):
    """
    Display state of a cell for the UI.

    Values (display priority):
        HIT_SHIP: Hit ship cell (red)
        HIT_MINE: Hit mine cell (💣 on black)
        MISS: Missed shot (black)
        SHIP: Unhit occupied ship cell (gray)
        EMPTY: Empty cell (white)
    """
    EMPTY = 0
    SHIP = 1
    HIT_SHIP = 2
    MISS = 3
    HIT_MINE = 4
    MINE = 5


class Cell:
    """
    Represents a single cell on the game board.

    Manages the state of an individual board cell including occupancy,
    shot status, and visual markers for game interaction.

    Attributes:
        x: X coordinate of the cell (column)
        y: Y coordinate of the cell (row)
        object: Occupying game object (ship/mine) or None
        is_shot: Whether this cell has been shot at
        is_adjacent: Temporary marker for adjacent cells (e.g., hover preview)
    """
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.object: GameObject | None = None
        self.is_shot: bool = False
        self.is_adjacent: bool = False

    def place_object(self, obj: GameObject):
        """
        Place a game object on this cell.

        Args:
            obj: The game object to place on this cell
        """
        self.object = obj
        obj.is_placed = True

    def mark_adjacent(self):
        """
        Mark this cell as adjacent for visual preview purposes.
        """
        self.is_adjacent = True

    def clear_adjacent(self):
        """
        Clear the adjacent marker from this cell.
        """
        self.is_adjacent = False

    def shoot(self) -> ShootResult:
        """
        Execute a shot on this cell.

        Marks the cell as shot and triggers hit handling if an object is present.

        Returns:
            ShootResult: Result of the shot (hit/miss with additional information)
        """
        self.is_shot = True
        if self.object:
            return ShootResult(True, self.object.on_hit(self.x, self.y), False, self.object)
        return ShootResult.miss()

    @property
    def is_occupied(self) -> bool:
        return self.object is not None

    @property
    def is_hit(self) -> bool:
        """
        Check if the cell has been hit and contains an object.

        Returns:
            bool: True if the cell was hit and contains an object, False otherwise
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
        """
        Determine the UI-relevant state of this cell.

        The priority follows the existing display logic:
        - First distinguish hit cases (ship > mine)
        - Then missed shots
        - Then visible ships
        - Otherwise empty

        Returns:
            CellState: Processed display state for the UI
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

