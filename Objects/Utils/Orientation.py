from enum import Enum


class Orientation(Enum):
    HORIZONTAL = 0
    VERTICAL = 1

    def rotate(self):
        self = not self
        return not self