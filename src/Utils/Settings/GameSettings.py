from dataclasses import dataclass
from typing import Optional, Any

from src.Utils.Enums.Constants import PlayerType, GameMode, GameConstants


@dataclass
class GameSettings:
    """
    Data model for game configuration settings.
    
    This dataclass holds all game configuration parameters including
    player types, names, difficulty levels, and game mode settings.
    Uses enums from constants.py for type safety and consistency.
    
    Attributes:
        p1_type: Player 1 type (Human or Computer)
        p2_type: Player 2 type (Human or Computer) 
        p1_name: Player 1 display name
        p2_name: Player 2 display name
        p1_difficulty: Player 1 difficulty level (for computer players)
        p2_difficulty: Player 2 difficulty level (for computer players)
        mode: Game mode (Standard or Extended)
        game_objects: Game objects configuration (set by Game later)
    """
    
    p1_type: str = GameConstants.DEFAULT_PLAYER1_TYPE
    p2_type: str = GameConstants.DEFAULT_PLAYER2_TYPE
    p1_name: str = GameConstants.DEFAULT_PLAYER1_NAME
    p2_name: str = GameConstants.DEFAULT_PLAYER2_NAME
    p1_difficulty: str = GameConstants.DEFAULT_PLAYER1_DIFFICULTY
    p2_difficulty: str = GameConstants.DEFAULT_PLAYER2_DIFFICULTY
    mode: str = GameConstants.DEFAULT_GAME_MODE
    game_objects: Optional[Any] = None  # Will be set later by Game
    
    def is_player_human(self, player_num: int) -> bool:
        """
        Check if a specific player is human.
        
        Args:
            player_num: Player number (1 or 2)
            
        Returns:
            bool: True if the player is human, False if computer
        """
        if player_num == 1:
            return self.p1_type == PlayerType.HUMAN.value
        elif player_num == 2:
            return self.p2_type == PlayerType.HUMAN.value
        else:
            raise ValueError(f"Invalid player number: {player_num}")
    
    def get_player_name(self, player_num: int) -> str:
        """
        Get the name of a specific player.
        
        Args:
            player_num: Player number (1 or 2)
            
        Returns:
            str: The player's name
        """
        if player_num == 1:
            return self.p1_name
        elif player_num == 2:
            return self.p2_name
        else:
            raise ValueError(f"Invalid player number: {player_num}")
    
    def get_player_difficulty(self, player_num: int) -> str:
        """
        Get the difficulty level of a specific player.
        
        Args:
            player_num: Player number (1 or 2)
            
        Returns:
            str: The player's difficulty level
        """
        if player_num == 1:
            return self.p1_difficulty
        elif player_num == 2:
            return self.p2_difficulty
        else:
            raise ValueError(f"Invalid player number: {player_num}")
    
    def is_extended_mode(self) -> bool:
        """
        Check if extended game mode is enabled.
        
        Returns:
            bool: True if extended mode is active, False for standard mode
        """
        return self.mode == GameMode.EXTENDED.value