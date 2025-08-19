from abc import ABC, abstractmethod
from typing import Tuple, List, TYPE_CHECKING

from Player.Player import Player

if TYPE_CHECKING:
    from Board.Board import Board
    from Objects.GameObject import GameObject


class ComputerPlayer(Player, ABC):
    """
    Abstract base class for computer-controlled players in the Battleships game.
    
    This class provides common functionality for all computer players, including
    target management and automatic object placement. Subclasses must implement
    the target selection strategy.
    
    Attributes:
        name (str): The player's display name
        board (Board): The player's game board where objects are placed
        objects (List): List of game objects (ships, mines) owned by this player
        available_targets (List[Tuple[int, int]]): List of coordinates that can still be targeted
    """
    
    def __init__(self, name: str, board: Board) -> None:
        """
        Initialize a new ComputerPlayer instance.
        
        Args:
            name: The player's display name
            board: The player's game board instance
        """
        super().__init__(name, board)
        self.available_targets: List[Tuple[int, int]] = [
            (x, y) for x in range(board.width) for y in range(board.height)
        ]

    @abstractmethod
    def select_target(self) -> Tuple[int, int]:
        """
        Abstract method to select the next target coordinate to shoot at.
        
        This method must be implemented by subclasses to define their
        targeting strategy (easy, hard, impossible difficulty).
        
        Returns:
            Tuple[int, int]: The (x, y) coordinates of the selected target
        """
        pass

    def place_object(self, game_object: GameObject) -> bool:
        """
        Place a game object using automatic placement logic.
        
        Computer players use the inherited method from Player
        to automatically place objects at valid positions.
        
        Args:
            game_object: The game object to place
            
        Returns:
            bool: True if the object was successfully placed, False otherwise
        """
        return self.place_random(game_object)
