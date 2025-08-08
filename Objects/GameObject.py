import abc
from abc import ABC
from enum import Enum

from Objects.Utils.Orientation import Orientation


class GameObject(ABC):
    def __init__(self, name: str, size: int, orientation: Orientation, coordinates: list[tuple[int, int]] = None):
        self.name = name
        self.size = size
        self.coordinates = coordinates if coordinates else []
        self.is_placed = False
        self.orientation = Orientation.HORIZONTAL  # default, falls relevant

    def set_position(self, start_x: int, start_y: int):
        if self.orientation == Orientation.HORIZONTAL:
            self.coordinates = [(start_x + i, start_y) for i in range(self.size)]
        else:  # Orientation.VERTICAL
            self.coordinates = [(start_x, start_y + i) for i in range(self.size)]

    @abc.abstractmethod
    def on_hit(self, x, y):  # bei Treffer
        pass

    @property
    @abc.abstractmethod
    def is_destroyed(self) -> bool:
        pass

    def rotate(self):
        self.orientation.rotate()

    @property
    @abc.abstractmethod
    def image(self):
        pass