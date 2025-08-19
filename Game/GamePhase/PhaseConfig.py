from dataclasses import dataclass, replace
from typing import Callable, Optional, Dict, Any

from Game.SettingsView import GameSettings
from Player.Player import Player
from Utils.GameState import GameState


@dataclass
class PhaseConfig:
    """
    Configuration object for game phases that encapsulates all initialization parameters.
    
    This DataClass reduces code duplication by centralizing phase initialization parameters
    instead of passing them individually through each phase constructor.
    
    Attributes:
        state: The current game state
        player1: First player instance
        player2: Second player instance
        turn_callback: Callback function for turn handling
        next_phase_callback: Callback function for phase transitions
        settings: Optional dictionary with game settings
    """
    state: GameState
    player1: Player
    player2: Player
    turn_callback: Callable
    next_phase_callback: Callable
    settings: GameSettings = None
    
    def with_changes(self, **kwargs) -> 'PhaseConfig':
        """
        Create a new PhaseConfig instance with specified changes.
        
        This method allows reusing most of the configuration while only updating
        the fields that need to change, avoiding the need to recreate the entire
        config object for phase transitions.
        
        Args:
            **kwargs: Fields to update (e.g., state=GameState.Shooting, turn_callback=new_callback)
            
        Returns:
            PhaseConfig: New instance with the specified changes
        """
        return replace(self, **kwargs)