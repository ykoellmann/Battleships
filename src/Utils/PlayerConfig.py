"""
Player configuration data model for the Battleships game.

This module contains the configuration data model for player creation,
providing a clean interface for the PlayerFactory pattern.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class PlayerConfig:
    """
    Configuration data model for player creation.
    
    This dataclass encapsulates all parameters needed to create a player
    instance through the PlayerFactory, providing better type safety and
    cleaner parameter passing.
    
    Attributes:
        player_type: Type of player (Human or Computer)
        name: Display name for the player
        difficulty: Difficulty level for computer players
        board: Player's own game board
        opponent_board: Opponent's game board (for AI strategy)
    """
    
    player_type: str
    name: str
    difficulty: str
    board: 'Board'
    opponent_board: Optional['Board'] = None
    
    def is_human(self) -> bool:
        """
        Check if this configuration is for a human player.
        
        Returns:
            bool: True if player type is human, False otherwise
        """
        from src.Utils.Constants import PlayerType
        return self.player_type == PlayerType.HUMAN.value
    
    def is_computer(self) -> bool:
        """
        Check if this configuration is for a computer player.
        
        Returns:
            bool: True if player type is computer, False otherwise
        """
        from src.Utils.Constants import PlayerType
        return self.player_type == PlayerType.COMPUTER.value
    
    def get_difficulty_level(self) -> str:
        """
        Get the difficulty level for computer players.
        
        Returns:
            str: The difficulty level string
        """
        return self.difficulty