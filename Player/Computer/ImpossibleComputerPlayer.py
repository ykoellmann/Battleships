import random

from Board.Board import Board
from Player.Computer.ComputerPlayer import ComputerPlayer


class ImpossibleComputerPlayer(ComputerPlayer):
    def __init__(self, board: Board, opponent_board: Board):
        super().__init__("Impossible Computer", board)
        self.opponent_board = opponent_board

    def select_target(self):
        target = random.choice(self.available_targets)
        self.available_targets.remove(target)
        return target

    @property
    def available_targets(self):
        if not self._available_targets:
            self._available_targets = [
                (x, y)
                for x in range(self.board.width)
                for y in range(self.board.height)
                if self.opponent_board.get_cell(x, y).is_occupied
            ]
        return self.available_targets

    @available_targets.setter
    def available_targets(self, value):
        self._available_targets = value