from collections import abc


class Player:
    def __init__(self, name: str, board):
        self.name = name
        self.board = board
        self.objects = []

    @abc.abstractmethod
    def place_object(self, game_object):
        pass

    @abc.abstractmethod
    def select_target(self):
        pass

    @property
    def has_lost(self):
        return all(obj.is_destroyed() for obj in self.objects)
