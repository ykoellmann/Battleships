import random
from collections import abc

from Objects.Utils.Orientation import Orientation
from Player.Player import Player


class ComputerPlayer(Player):
    def __init__(self, name: str, board):
        super().__init__(name, board)
        self.available_targets = [(x, y) for x in range(board.width) for y in range(board.height)]

    @abc.abstractmethod
    def select_target(self) -> tuple[int, int]:
        pass

    def get_all_valid_positions(self, board, ship_length, game_object):
        positions = []
        for row in range(10):
            for col in range(10):
                for direction in ["horizontal", "vertical"]:
                    if self.can_place(board, row, col, ship_length, direction, game_object):
                        positions.append((row, col, direction))
        return positions

    def can_place(self, board, row, col, ship_length, direction, game_object):
        # Setze Orientierung und Position temporär
        if direction == "horizontal":
            game_object.orientation = Orientation.HORIZONTAL
        else:
            game_object.orientation = Orientation.VERTICAL
        game_object.set_position(row, col)
        return board.can_place_object(game_object)

    def place_safely(self, board, ship_length, game_object):
        valid_positions = self.get_all_valid_positions(board, ship_length, game_object)
        if not valid_positions:
            return False
        row, col, direction = random.choice(valid_positions)
        if direction == "horizontal":
            game_object.orientation = Orientation.HORIZONTAL
        else:
            game_object.orientation = Orientation.VERTICAL
        game_object.set_position(row, col)
        return board.place_object(game_object)

    def place_object(self, game_object):
        ship_length = len(game_object.coordinates)
        placed = self.place_safely(self.board, ship_length, game_object)
        # Falls keine Position gefunden, mache nichts (sollte aber nie passieren)
        return placed
