import random
from typing import List, Optional
from Player.Computer.ComputerPlayer import ComputerPlayer
from Utils.Orientation import Orientation


class HardComputerPlayer(ComputerPlayer):
    def __init__(self, board):
        super().__init__("Hard Computer", board)
        self.search_queue: list[tuple[int, int]] = []
        self.current_direction = None
        self.first_hit = None

    def select_target(self) -> tuple[int, int] | None:
        if self.search_queue:
            target = self.search_queue.pop(0)
            if target in self.available_targets:
                self.available_targets.remove(target)
            else:
                return self.select_target()
            return target

        if self.available_targets:
            target = random.choice(self.available_targets)
            self.available_targets.remove(target)
            return target
        return None

    def process_shot_result(self, x: int, y: int, was_hit: bool, ship_destroyed: bool = False, destroyed_ship_cells: List[tuple[int, int]] = None):
        """
        destroyed_ship_cells = Liste aller Koordinaten des versenkten Schiffs,
        damit wir angrenzende Felder blockieren können.
        """
        if not was_hit:
            if self.current_direction and self.first_hit:
                opp_dx, opp_dy = -self.current_direction[0], -self.current_direction[1]
                nx, ny = self.first_hit[0] + opp_dx, self.first_hit[1] + opp_dy
                if (nx, ny) in self.available_targets and (nx, ny) not in self.search_queue:
                    self.search_queue.insert(0, (nx, ny))
                self.current_direction = None
            return

        if ship_destroyed:
            self.search_queue.clear()
            self.current_direction = None
            self.first_hit = None

            # Neue Logik: angrenzende Felder entfernen
            if destroyed_ship_cells:
                for cell in destroyed_ship_cells:
                    for nx, ny in self.get_surrounding_cells(*cell):
                        if (nx, ny) in self.available_targets:
                            self.available_targets.remove((nx, ny))
            return

        if not self.first_hit:
            self.first_hit = (x, y)
            self.search_queue.extend(self.get_valid_neighbors(x, y, None))
        else:
            if not self.current_direction:
                if x == self.first_hit[0]:
                    self.current_direction = (0, 1) if y > self.first_hit[1] else (0, -1)
                else:
                    self.current_direction = (1, 0) if x > self.first_hit[0] else (-1, 0)

            if self.current_direction:
                nx, ny = x + self.current_direction[0], y + self.current_direction[1]
                if (nx, ny) in self.available_targets:
                    self.search_queue.insert(0, (nx, ny))

    def get_valid_neighbors(self, x: int, y: int, direction) -> list[tuple[int, int]]:
        neighbors = []
        directions = []

        if direction == Orientation.HORIZONTAL or direction is None:
            directions.extend([(1, 0), (-1, 0)])
        if direction == Orientation.VERTICAL or direction is None:
            directions.extend([(0, 1), (0, -1)])

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (
                    0 <= nx < self.board.width
                    and 0 <= ny < self.board.height
                    and (nx, ny) in self.available_targets
                    and (nx, ny) not in self.search_queue
            ):
                neighbors.append((nx, ny))
        return neighbors

    def get_surrounding_cells(self, x: int, y: int) -> list[tuple[int, int]]:
        """Alle 8 Felder um eine Zelle herum zurückgeben (inkl. Diagonalen)."""
        cells = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.board.width and 0 <= ny < self.board.height:
                    cells.append((nx, ny))
        return cells