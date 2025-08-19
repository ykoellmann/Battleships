import random
from typing import Tuple, Optional, TYPE_CHECKING

from Player.Computer.ComputerPlayer import ComputerPlayer

if TYPE_CHECKING:
    from Board.Board import Board


class ImpossibleComputerPlayer(ComputerPlayer):
    """
    Impossible difficulty computer player implementation.
    
    This computer player uses perfect information (cheating) by having access
    to the opponent's board. It only targets cells that contain ships, making
    it virtually impossible to beat. This provides the ultimate challenge mode
    for testing purposes.
    
    Note: This implementation "cheats" by accessing opponent board information
    that would not be available in a real game scenario.
    
    Attributes:
        name (str): Always "Impossible Computer"
        board (Board): The player's game board where objects are placed
        objects (List): List of game objects (ships, mines) owned by this player
        available_targets (List[Tuple[int, int]]): List of coordinates that can still be targeted
        opponent_board (Board): Reference to opponent's board for perfect targeting
    """
    
    def __init__(self, board: Board, opponent_board: Board) -> None:
        """
        Initialize a new ImpossibleComputerPlayer instance.
        
        Args:
            board: The player's game board instance
            opponent_board: The opponent's board for perfect information targeting
        """
        super().__init__("Impossible Computer", board)
        self.opponent_board = opponent_board
        self.refresh_available_targets()

    def select_target(self) -> Optional[Tuple[int, int]]:
        """
        Select a target using perfect information (cheating).
        
        This method only targets cells that are known to contain ships,
        making it impossible to miss. If no targets are available,
        it refreshes the target list.
        
        Returns:
            Optional[Tuple[int, int]]: The (x, y) coordinates of a cell containing a ship,
                                     or None if no ships remain
        """
        if not self.available_targets:
            self.refresh_available_targets()
        if not self.available_targets:
            return None
        target = random.choice(self.available_targets)
        self.available_targets.remove(target)
        return target

    def refresh_available_targets(self) -> None:
        """
        Refresh the list of available targets by scanning opponent's board.
        
        This method cheats by examining the opponent's board directly
        and only adding cells that contain ships to the target list.
        This ensures 100% hit rate.
        """
        self.available_targets = [
            (x, y)
            for x in range(self.board.width)
            for y in range(self.board.height)
            if self.opponent_board.get_cell(x, y).is_occupied
        ]