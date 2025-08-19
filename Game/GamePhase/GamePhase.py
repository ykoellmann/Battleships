import abc
from abc import ABC

from Player.Player import Player
from Utils.GameState import GameState
from Game.GamePhase.PhaseConfig import PhaseConfig


class GamePhase(ABC):
    def __init__(self, config: PhaseConfig):
        """
        Initialize the GamePhase with a configuration object.
        
        Args:
            config: PhaseConfig object containing all initialization parameters
        """
        self.state = config.state
        self.turn_callback = config.turn_callback
        self.players = [config.player1, config.player2]
        self.current_player_idx = 0
        self.settings = config.settings
        self.next_phase_callback = config.next_phase_callback

    @abc.abstractmethod
    def handle_cell_click(self, x, y, is_own_board):
        pass

    @abc.abstractmethod
    def execute_turn(self, x, y):
        pass

    @abc.abstractmethod
    def next_turn(self):
        pass

    @abc.abstractmethod
    def is_over(self):
        pass

    @abc.abstractmethod
    def next_phase(self):
        pass


    def next_player(self):
        """Wechselt den aktiven Spieler und aktualisiert die Phase."""
        placement_done = self.current_player_idx == 1
        self.current_player_idx = 1 - self.current_player_idx
        return placement_done

    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_idx]

    @property
    def other_player(self) -> Player:
        return self.players[1 - self.current_player_idx]

    @property
    def game_over(self) -> bool:
        return any(player.has_lost for player in self.players)