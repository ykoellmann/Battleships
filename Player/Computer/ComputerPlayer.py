from abc import ABC
from Player.Player import Player
import abc
import random
from Utils.Orientation import Orientation

class ComputerPlayer(Player, ABC):
    def __init__(self, name: str, board):
        super().__init__(name, board)
        self.available_targets = [(x, y) for x in range(board.width) for y in range(board.height)]

    @abc.abstractmethod
    def select_target(self) -> tuple[int, int]:
        pass

    def place_object(self, game_object):
        return self.place_random(game_object)
