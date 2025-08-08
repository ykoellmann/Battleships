from random import random
from typing import List, Optional

from Player.Computer.ComputerPlayer import ComputerPlayer


class HardComputerPlayer(ComputerPlayer):
    def __init__(self, board):
        super().__init__("Hard Computer", board)
        self.hit_stack: List[tuple[int, int]] = []  # Treffer-Koordinaten merken
        self.search_queue: List[tuple[int, int]] = []  # Nachbarn, die geprüft werden
        self.last_hit: Optional[tuple[int, int]] = None

    def select_target(self) -> tuple[int, int]:
        # Wenn wir gezielt nach Schiffsteilen suchen
        if self.search_queue:
            target = self.search_queue.pop(0)
            if target in self.available_targets:
                self.available_targets.remove(target)
            else:
                # Ziel schon beschossen, nächstes versuchen
                return self.select_target()
            return target

        # Kein aktueller Treffer → zufälliger Schuss
        if self.available_targets:
            target = random.choice(self.available_targets)
            self.available_targets.remove(target)
            return target
        return None

    def process_shot_result(self, x: int, y: int, was_hit: bool, ship_destroyed: bool = False):
        if was_hit:
            self.hit_stack.append((x, y))
            # Füge Nachbarzellen für gezieltes Schießen hinzu
            neighbors = self.get_valid_neighbors(x, y)
            for n in neighbors:
                if n in self.available_targets and n not in self.search_queue:
                    self.search_queue.append(n)

            if ship_destroyed:
                # Schiff versenkt → Suche zurücksetzen
                self.hit_stack.clear()
                self.search_queue.clear()

    def get_valid_neighbors(self, x: int, y: int) -> List[tuple[int, int]]:
        neighbors = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # horizontal + vertikal
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.board.width and 0 <= ny < self.board.height:
                neighbors.append((nx, ny))
        return neighbors