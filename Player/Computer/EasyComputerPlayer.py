import random
from typing import Optional, Tuple

from Player.Computer.ComputerPlayer import ComputerPlayer

from Board.Board import Board


class EasyComputerPlayer(ComputerPlayer):
    """
    Easy difficulty computer player implementation.
    
    This computer player uses a completely random targeting strategy,
    selecting targets at random from all available positions. This provides
    the easiest difficulty level for human players to compete against.
    
    Attributes:
        name (str): Always "Easy Computer" 
        board (Board): The player's game board where objects are placed
        objects (List): List of game objects (ships, mines) owned by this player
        available_targets (List[Tuple[int, int]]): List of coordinates that can still be targeted
    """
    
    def __init__(self, board: Board) -> None:
        """
        Initialize a new EasyComputerPlayer instance.
        
        Args:
            board: The player's game board instance
        """
        super().__init__("Easy Computer", board)

    def select_target(self) -> Optional[Tuple[int, int]]:
        """
        Select a random target from available positions.
        
        The easy computer player uses pure randomness for target selection,
        making it the least challenging opponent. Once a target is selected,
        it is removed from available targets to avoid duplicate shots.
        
        Returns:
            Optional[Tuple[int, int]]: The (x, y) coordinates of the selected target,
                                     or None if no targets are available
        """
        if not self.available_targets:
            return None
        target = random.choice(self.available_targets)
        self.available_targets.remove(target)
        return target