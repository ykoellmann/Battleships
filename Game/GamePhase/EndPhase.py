from Game.GamePhase.GamePhase import GamePhase
from Utils.GameState import GameState


class EndPhase(GamePhase):

    def __init__(self, player1, player2, turn_callback):
        super().__init__(GameState.End, player1, player2, turn_callback)

    def execute_turn(self, x, y):
        pass

    def next_turn(self):
        self.turn_callback()

    def is_over(self):
        return True

    def handle_cell_click(self, x, y):
        pass