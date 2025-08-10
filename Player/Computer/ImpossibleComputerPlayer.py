import random

from Board.Board import Board
from Player.Computer.ComputerPlayer import ComputerPlayer


class ImpossibleComputerPlayer(ComputerPlayer):
    def __init__(self, board: Board, opponent_board: Board):
        super().__init__("Impossible Computer", board)
        self.opponent_board = opponent_board
        self.refresh_available_targets()

    def select_target(self):
        if not self.available_targets:
            self.refresh_available_targets()
        target = random.choice(self.available_targets)
        self.available_targets.remove(target)
        return target

    def refresh_available_targets(self):
        self.available_targets = [
            (x, y)
            for x in range(self.board.width)
            for y in range(self.board.height)
            if self.opponent_board.get_cell(x, y).is_occupied
        ]