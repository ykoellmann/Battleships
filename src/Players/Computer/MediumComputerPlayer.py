import random
from typing import List, Optional, Tuple

from src.Players.Computer.ComputerPlayer import ComputerPlayer
from src.Utils.Enums.Orientation import Orientation

from src.Core.Board.Board import Board


class MediumComputerPlayer(ComputerPlayer):
    """
    Medium difficulty computer player implementation.
    
    This computer player uses an intelligent hunting strategy. When it hits a ship,
    it systematically searches adjacent cells to find and destroy the entire ship.
    It also removes surrounding cells from targeting when a ship is destroyed
    to optimize targeting efficiency.
    
    Attributes:
        name (str): Always "Mittel Computer"
        board (Board): The player's game board where objects are placed
        objects (List): List of game objects (ships, mines) owned by this player
        available_targets (List[Tuple[int, int]]): List of coordinates that can still be targeted
        search_queue (List[Tuple[int, int]]): Queue of high-priority targets around hit ships
        current_direction (Optional[Tuple[int, int]]): Current search direction when following a ship
        first_hit (Optional[Tuple[int, int]]): Coordinates of the first hit on current target ship
    """
    
    def __init__(self, board: Board) -> None:
        """
        Initialize a new HardComputerPlayer instance.
        
        Args:
            board: The player's game board instance
        """
        super().__init__("Mittlerer Computer", board)
        self.search_queue: List[Tuple[int, int]] = []
        self.current_direction: Optional[Tuple[int, int]] = None
        self.first_hit: Optional[Tuple[int, int]] = None

    def select_target(self) -> Optional[Tuple[int, int]]:
        """
        Select the next target using intelligent hunting strategy.
        
        Priority order:
        1. Targets from search_queue (adjacent to known hits)
        2. Random targets from available_targets
        
        Returns:
            Optional[Tuple[int, int]]: The (x, y) coordinates of the selected target,
                                     or None if no targets are available
        """
        if self.search_queue:
            target = self.search_queue.pop(0)
            if target in self.available_targets:
                self.available_targets.remove(target)
            else:
                return self.select_target()
            return target

        if self.available_targets:
            target = random.choice(self.available_targets)
            self.available_targets.remove(target)
            return target
        return None

    def process_shot_result(self, x: int, y: int, was_hit: bool, ship_destroyed: bool = False, 
                          destroyed_ship_cells: Optional[List[Tuple[int, int]]] = None) -> None:
        """
        Process the result of a shot to update targeting strategy.
        
        This method implements the intelligent hunting behavior:
        - On miss: Try opposite direction if following a ship
        - On hit: Add adjacent cells to search queue
        - On ship destroyed: Clear search state and remove surrounding cells
        
        Args:
            x: X coordinate of the shot
            y: Y coordinate of the shot  
            was_hit: Whether the shot was a hit
            ship_destroyed: Whether the hit destroyed a ship
            destroyed_ship_cells: List of all coordinates of the destroyed ship
        """
        if not was_hit:
            if self.current_direction and self.first_hit:
                opp_dx, opp_dy = -self.current_direction[0], -self.current_direction[1]
                nx, ny = self.first_hit[0] + opp_dx, self.first_hit[1] + opp_dy
                if (nx, ny) in self.available_targets and (nx, ny) not in self.search_queue:
                    self.search_queue.insert(0, (nx, ny))
                self.current_direction = None
            return

        if ship_destroyed:
            self.search_queue.clear()
            self.current_direction = None
            self.first_hit = None

            # Neue Logik: angrenzende Felder entfernen
            if destroyed_ship_cells:
                for cell in destroyed_ship_cells:
                    for nx, ny in self.get_surrounding_cells(*cell):
                        if (nx, ny) in self.available_targets:
                            self.available_targets.remove((nx, ny))
            return

        if not self.first_hit:
            self.first_hit = (x, y)
            self.search_queue.extend(self.get_valid_neighbors(x, y, None))
        else:
            if not self.current_direction:
                if x == self.first_hit[0]:
                    self.current_direction = (0, 1) if y > self.first_hit[1] else (0, -1)
                else:
                    self.current_direction = (1, 0) if x > self.first_hit[0] else (-1, 0)

            if self.current_direction:
                nx, ny = x + self.current_direction[0], y + self.current_direction[1]
                if (nx, ny) in self.available_targets:
                    self.search_queue.insert(0, (nx, ny))

    def get_valid_neighbors(self, x: int, y: int, direction: Optional[Orientation]) -> List[Tuple[int, int]]:
        """
        Get valid neighboring cells for targeting based on ship orientation.
        
        This method finds adjacent cells that are valid targets, considering
        ship orientation constraints. For unknown orientation, it checks all
        four cardinal directions.
        
        Args:
            x: X coordinate of the reference cell
            y: Y coordinate of the reference cell
            direction: Known ship orientation, or None if unknown
            
        Returns:
            List[Tuple[int, int]]: List of valid neighboring coordinates
        """
        neighbors = []
        directions = []

        if direction == Orientation.HORIZONTAL or direction is None:
            directions.extend([(1, 0), (-1, 0)])
        if direction == Orientation.VERTICAL or direction is None:
            directions.extend([(0, 1), (0, -1)])

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (
                    0 <= nx < self.board.width
                    and 0 <= ny < self.board.height
                    and (nx, ny) in self.available_targets
                    and (nx, ny) not in self.search_queue
            ):
                neighbors.append((nx, ny))
        return neighbors

    def get_surrounding_cells(self, x: int, y: int) -> List[Tuple[int, int]]:
        """
        Get all 8 surrounding cells around a given position (including diagonals).
        
        This method is used to mark cells around destroyed ships as unavailable
        for targeting, since ships cannot be placed adjacent to each other.
        
        Args:
            x: X coordinate of the center cell
            y: Y coordinate of the center cell
            
        Returns:
            List[Tuple[int, int]]: List of surrounding cell coordinates within board bounds
        """
        cells = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.board.width and 0 <= ny < self.board.height:
                    cells.append((nx, ny))
        return cells