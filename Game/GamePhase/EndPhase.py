from Game.GamePhase.GamePhase import GamePhase
from Game.GamePhase.PhaseConfig import PhaseConfig
from Utils.GameState import GameState


class EndPhase(GamePhase):

    def __init__(self, config: PhaseConfig):
        """
        Initialize the EndPhase with configuration.
        
        This phase represents the end state of the game when one player has won.
        
        Args:
            config: PhaseConfig object containing all initialization parameters
        """
        super().__init__(config)

    def execute_turn(self, x, y):
        pass

    def next_turn(self):
        self.turn_callback()

    def is_over(self):
        return True

    def handle_cell_click(self, x, y, is_own_board):
        pass

    def next_phase(self):
        pass