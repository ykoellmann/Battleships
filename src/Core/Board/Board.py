from src.Core.Board.Cell import Cell
from src.Core.Entities.GameObject import GameObject
from src.Utils.ShootResult import ShootResult


class Board:
    """
    Game board logic consisting of a 2D grid of Cell objects.

    Manages the placement and interaction of game objects on a grid-based
    board. Handles object placement validation, adjacency rules, and
    shooting mechanics.

    Attributes:
        width: Board width in cells
        height: Board height in cells  
        grid: 2D list of all cells
        objects: List of all placed game objects
    """
    def __init__(self, width: int = 10, height: int = 10):
        self.width = width
        self.height = height
        self.grid: list[list[Cell]] = [
            [Cell(x, y) for y in range(height)] for x in range(width)
        ]
        self.objects: list[GameObject] = []

    def get_cell(self, x: int, y: int) -> Cell | None:
        """
        Get the cell at position (x, y) if within board bounds.

        Args:
            x: Column index
            y: Row index

        Returns:
            Cell | None: The cell at the specified position, or None if out of bounds
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[x][y]
        return None

    def can_place_object(self, obj: GameObject) -> bool:
        """
        Check if a game object can be placed on the board.

        Validates placement by ensuring all target cells are within bounds
        and free, and that no adjacent cells (including diagonals) are occupied.

        Args:
            obj: The game object to place with coordinates already set

        Returns:
            bool: True if placement is possible, False otherwise
        """
        for x, y in obj.coordinates:
            cell = self.get_cell(x, y)
            if not cell or cell.is_occupied:
                return False
        
        for cell in self._get_adjacent_cells(obj):
            if cell.is_occupied:
                return False
        return True

    def place_object(self, obj: GameObject) -> bool:
        """
        Place an object on the board if the placement is valid.

        Args:
            obj: The game object to place with coordinates already set

        Returns:
            bool: True if placement was successful, False otherwise
        """
        if not self.can_place_object(obj):
            return False

        for x, y in obj.coordinates:
            self.get_cell(x, y).place_object(obj)

        obj.is_placed = True
        self.objects.append(obj)
        return True

    def remove_object(self, obj: GameObject):
        """
        Remove a previously placed object from the board and clean up state.

        Args:
            obj: The game object to remove
        """
        for x, y in obj.coordinates:
            cell = self.get_cell(x, y)
            if cell and cell.object == obj:
                cell.object = None

        obj.is_placed = False
        if obj in self.objects:
            self.objects.remove(obj)

    def _get_adjacent_cells(self, obj: GameObject) -> list[Cell]:
        """
        Get all adjacent cells (including diagonals) to an object's coordinates.

        Args:
            obj: Game object whose surroundings are checked

        Returns:
            list[Cell]: List of adjacent cells within board bounds
        """
        adjacent = set()

        for x, y in obj.coordinates:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    ax, ay = x + dx, y + dy
                    if (dx == 0 and dy == 0) or not (0 <= ax < self.width and 0 <= ay < self.height):
                        continue
                    adjacent.add(self.get_cell(ax, ay))

        return list(adjacent)

    def _clear_all_adjacent_markers(self):
        """
        Remove all temporary adjacent markers from all cells.
        """
        for row in self.grid:
            for cell in row:
                cell.clear_adjacent()

    def _mark_adjacent_for_object(self, obj: GameObject):
        """
        Mark free adjacent cells around an object for visual preview.

        Args:
            obj: Game object whose adjacent cells should be marked
        """
        for cell in self._get_adjacent_cells(obj):
            if not cell.is_occupied:
                cell.mark_adjacent()

    def shoot_at(self, x: int, y: int) -> ShootResult:
        """
        Execute a shot at cell (x, y) if valid.

        Args:
            x: Column index
            y: Row index

        Returns:
            ShootResult: Result of the shot attempt
        """
        cell = self.get_cell(x, y)
        if not cell or cell.is_shot:
            return ShootResult(False, False, cell is None)
        return cell.shoot()