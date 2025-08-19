from abc import ABC, abstractmethod
from typing import List, Callable, Optional

from src.Utils.GameState import GameState
from src.Core.GamePhases.PhaseConfig import PhaseConfig

from src.Players.Player import Player
from src.Views.SettingsView import GameSettings


class GamePhase(ABC):
    """
    Abstract base class for all game phases in the Battleships game.
    
    This class defines the common interface and functionality for all game phases
    including placement, shooting, and end phases. Each phase manages the game
    flow, player interactions, and state transitions.
    
    Attributes:
        state (GameState): Current game state/phase
        turn_callback (Callable): Callback function for turn handling
        players (List[Player]): List containing both players
        current_player_idx (int): Index of the currently active player (0 or 1)
        settings (GameSettings): Game configuration settings
        next_phase_callback (Callable): Callback function for phase transitions
    """
    
    def __init__(self, config: PhaseConfig) -> None:
        """
        Initialize the GamePhase with a configuration object.
        
        Args:
            config: PhaseConfig object containing all initialization parameters
        """
        self.state: GameState = config.state
        self.turn_callback: Callable = config.turn_callback
        self.players: List[Player] = [config.player1, config.player2]
        self.current_player_idx: int = 0
        self.settings: Optional[GameSettings] = config.settings
        self.next_phase_callback: Callable = config.next_phase_callback

    @abstractmethod
    def handle_cell_click(self, x: int, y: int, is_own_board: bool) -> None:
        """
        Abstract method to handle cell click events.
        
        Args:
            x: X coordinate of the clicked cell
            y: Y coordinate of the clicked cell
            is_own_board: True if clicking on own board, False for opponent board
        """
        pass

    @abstractmethod
    def execute_turn(self, x: int, y: int) -> bool:
        """
        Abstract method to execute a game turn action.
        
        Args:
            x: X coordinate for the action
            y: Y coordinate for the action
            
        Returns:
            bool: True if the action was successful, False otherwise
        """
        pass

    @abstractmethod
    def next_turn(self) -> None:
        """
        Abstract method to advance to the next turn.
        
        This method should handle turn progression logic and
        call appropriate callbacks.
        """
        pass

    @abstractmethod
    def is_over(self) -> bool:
        """
        Abstract method to check if the current phase is complete.
        
        Returns:
            bool: True if the phase should end, False otherwise
        """
        pass

    @abstractmethod
    def next_phase(self) -> None:
        """
        Abstract method to trigger transition to the next phase.
        
        This method should call the next_phase_callback with the
        appropriate next phase class.
        """
        pass

    def next_player(self) -> bool:
        """
        Switch to the next player and update the phase state.
        
        This method alternates between player 0 and player 1, and
        determines if a complete round (both players) has been completed.
        
        Returns:
            bool: True if both players have completed their turns, False otherwise
        """
        placement_done = self.current_player_idx == 1
        self.current_player_idx = 1 - self.current_player_idx
        return placement_done

    @property
    def current_player(self) -> Player:
        """
        Get the currently active player.
        
        Returns:
            Player: The player whose turn it currently is
        """
        return self.players[self.current_player_idx]

    @property
    def other_player(self) -> Player:
        """
        Get the non-active player (opponent).
        
        Returns:
            Player: The player who is not currently taking their turn
        """
        return self.players[1 - self.current_player_idx]

    @property
    def game_over(self) -> bool:
        """
        Check if the entire game is over.
        
        The game is over when any player has lost (all their objects destroyed).
        
        Returns:
            bool: True if the game is over, False if it should continue
        """
        return any(player.has_lost for player in self.players)