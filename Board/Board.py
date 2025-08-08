from Board.Cell import Cell
from Objects.GameObject import GameObject


class Board:
    def __init__(self, width: int = 10, height: int = 10):
        self.width = width
        self.height = height
        self.grid: list[list[Cell]] = [
            [Cell(x, y) for y in range(height)] for x in range(width)
        ]
        self.objects: list[GameObject] = []  # Alle platzierten Objekte

    def get_cell(self, x: int, y: int) -> Cell | None:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[x][y]
        return None

    def can_place_object(self, obj: GameObject) -> bool:
        for x, y in obj.coordinates:
            cell = self.get_cell(x, y)
            if not cell or cell.is_occupied():
                return False
        return True

    def place_object(self, obj: GameObject) -> bool:
        if not self.can_place_object(obj):
            return False

        for x, y in obj.coordinates:
            self.get_cell(x, y).place_object(obj)

        obj.is_placed = True
        self.objects.append(obj)
        return True

    def remove_object(self, obj: GameObject):
        for x, y in obj.coordinates:
            cell = self.get_cell(x, y)
            if cell and cell.object == obj:
                cell.object = None

        obj.is_placed = False
        if obj in self.objects:
            self.objects.remove(obj)

    def get_adjacent_cells(self, obj: GameObject) -> list[Cell]:
        adjacent = set()

        for x, y in obj.coordinates:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    ax, ay = x + dx, y + dy
                    if (dx == 0 and dy == 0) or not (0 <= ax < self.width and 0 <= ay < self.height):
                        continue
                    adjacent.add(self.get_cell(ax, ay))

        return list(adjacent)

    def clear_all_adjacent_markers(self):
        for row in self.grid:
            for cell in row:
                cell.clear_adjacent()

    def mark_adjacent_for_object(self, obj: GameObject):
        for cell in self.get_adjacent_cells(obj):
            if not cell.is_occupied():
                cell.mark_adjacent()

    def shoot_at(self, x: int, y: int) -> bool:
        cell = self.get_cell(x, y)
        if not cell or cell.is_shot:
            return False
        return cell.shoot()