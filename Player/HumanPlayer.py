from typing import TYPE_CHECKING

from Player.Player import Player

if TYPE_CHECKING:
    from Board.Board import Board
    from Objects.GameObject import GameObject


class HumanPlayer(Player):
    """
    Human player implementation for the Battleships game.
    
    This class represents a human player who manually places ships and makes moves
    through the user interface. Unlike computer players, human players require
    user input for all game actions.
    
    Attributes:
        name (str): The player's display name
        board (Board): The player's game board where objects are placed
        objects (List): List of game objects (ships, mines) owned by this player
    """
    
    def __init__(self, name: str, board: Board) -> None:
        """
        Initialize a new HumanPlayer instance.
        
        Args:
            name: The player's display name
            board: The player's game board instance
        """
        super().__init__(name, board)

    def place_object(self, game_object: GameObject) -> bool:
        """
        Place a game object on the player's board.
        
        For human players, this method checks if the placement is valid and
        places the object if possible. The placement position should be set
        on the game_object before calling this method.
        
        Args:
            game_object: The game object to place on the board
            
        Returns:
            bool: True if placement was successful, False if invalid placement
        """
        if self.board.can_place_object(game_object):
            self.objects.append(game_object)
            self.board.place_object(game_object)
            return True
        return False
