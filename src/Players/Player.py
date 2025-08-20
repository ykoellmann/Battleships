import random
from abc import abstractmethod, ABC
from typing import List, Tuple

from src.Core.Board.Board import Board
from src.Utils.Enums.Constants import BoardConfig
from src.Utils.Enums.Orientation import Orientation


class Player(ABC):
    """
    Abstract base class for all players in the Battleships game.
    
    This class defines the common interface and functionality for both human and computer players,
    including ship placement, game object management, and loss condition checking.
    
    Attributes:
        name (str): The player's display name
        board: The player's game board where objects are placed
        objects (List): List of game objects (ships, mines) owned by this player
    """
    
    def __init__(self, name: str, board: Board) -> None:
        """
        Initialize a new Player instance.
        
        Args:
            name: The player's display name
            board: The player's game board instance
        """
        self.name = name
        self.board = board
        self.objects: List = []

    @abstractmethod
    def place_object(self, game_object) -> bool:
        """
        Abstract method to place a game object on the player's board.
        
        Args:
            game_object: The game object to place
            
        Returns:
            bool: True if placement was successful, False otherwise
        """
        pass

    @property
    def has_lost(self) -> bool:
        """
        Check if the player has lost the game.
        
        A player has lost when all their objects are destroyed.
        
        Returns:
            bool: True if the player has lost, False otherwise
        """
        return all(obj.is_destroyed for obj in self.objects)

    def _get_all_valid_positions(self, board, ship_length: int, game_object) -> List[Tuple[int, int, str]]:
        """
        Get all valid positions for placing a game object (legacy method).
        
        Args:
            board: The board to place on
            ship_length: Length of the ship
            game_object: The game object to place
            
        Returns:
            List of tuples (row, col, direction) representing valid positions
        """
        positions = []
        for row in range(BoardConfig.DEFAULT_HEIGHT):
            for col in range(BoardConfig.DEFAULT_WIDTH):
                for direction in [Orientation.HORIZONTAL.value, Orientation.VERTICAL.value]:
                    if self._can_place(board, row, col, ship_length, direction, game_object):
                        positions.append((row, col, direction))
        return positions

    def _can_place(self, board, row: int, col: int, ship_length: int, direction: str, game_object) -> bool:
        """
        Check if a game object can be placed at the specified position.
        
        Args:
            board: The board to place on
            row: Row position
            col: Column position
            ship_length: Length of the ship
            direction: Direction ("horizontal" or "vertical")
            game_object: The game object to place
            
        Returns:
            bool: True if placement is valid, False otherwise
        """
        # Set orientation and position temporarily
        if direction == Orientation.HORIZONTAL.value:
            game_object.orientation = Orientation.HORIZONTAL
        else:
            game_object.orientation = Orientation.VERTICAL
        game_object.set_position(row, col)
        return board.can_place_object(game_object)

    def _place_safely(self, board, ship_length: int, game_object) -> bool:
        """
        Place a game object safely at a random valid position.
        
        Args:
            board: The board to place on
            ship_length: Length of the ship
            game_object: The game object to place
            
        Returns:
            bool: True if placement was successful, False otherwise
        """
        valid_positions = self._get_all_valid_positions(board, ship_length, game_object)
        if not valid_positions:
            return False
        row, col, direction = random.choice(valid_positions)
        if direction == Orientation.HORIZONTAL.value:
            game_object.orientation = Orientation.HORIZONTAL
        else:
            game_object.orientation = Orientation.VERTICAL
        game_object.set_position(row, col)
        return board.place_object(game_object)

    def place_random(self, game_object) -> bool:
        """
        Place a game object randomly on this player's board.
        
        Args:
            game_object: The game object to place
            
        Returns:
            bool: True if placement was successful, False otherwise
        """
        ship_length = len(game_object.coordinates)
        placed = self._place_safely(self.board, ship_length, game_object)
        self.objects.append(game_object)
        # Falls keine Position gefunden, mache nichts (sollte aber nie passieren)
        return placed