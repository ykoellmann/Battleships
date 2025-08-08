from random import random

from Board.Board import Board
from Player.Computer.ComputerPlayer import ComputerPlayer


class EasyComputerPlayer(ComputerPlayer):
    def __init__(self, board: Board):
        super().__init__("Easy Computer", board)

    def select_target(self):
        target = random.choice(self.available_targets)
        self.available_targets.remove(target)
        return target