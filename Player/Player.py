import random
from collections import abc

from Utils.Orientation import Orientation


class Player:
    def __init__(self, name: str, board):
        self.name = name
        self.board = board
        self.objects = []

    @abc.abstractmethod
    def place_object(self, game_object):
        pass

    @property
    def has_lost(self):
        return all(obj.is_destroyed for obj in self.objects)

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

    def place_random(self, game_object):
        ship_length = len(game_object.coordinates)
        placed = self.place_safely(self.board, ship_length, game_object)
        self.objects.append(game_object)
        # Falls keine Position gefunden, mache nichts (sollte aber nie passieren)
        return placed