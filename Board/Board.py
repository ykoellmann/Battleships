from dataclasses import dataclass

from Board.Cell import Cell
from Objects.GameObject import GameObject
from Utils.ShootResult import ShootResult


class Board:
    """
    Spielfeld-Logik bestehend aus einem 2D-Raster aus Cell-Objekten.

    Attribute:
        width (int): Breite des Boards in Zellen.
        height (int): Höhe des Boards in Zellen.
        grid (list[list[Cell]]): 2D-Liste aller Zellen.
        objects (list[GameObject]): Liste aller platzierten Spielobjekte.
    """
    def __init__(self, width: int = 10, height: int = 10):
        self.width = width
        self.height = height
        self.grid: list[list[Cell]] = [
            [Cell(x, y) for y in range(height)] for x in range(width)
        ]
        self.objects: list[GameObject] = []  # Alle platzierten Objekte

    def get_cell(self, x: int, y: int) -> Cell | None:
        """Gibt die Zelle an Position (x, y) zurück, falls innerhalb der Grenzen.

        Args:
            x (int): Spaltenindex.
            y (int): Zeilenindex.
        Returns:
            Cell | None: Die Zelle oder None, wenn außerhalb des Boards.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[x][y]
        return None

    def can_place_object(self, obj: GameObject) -> bool:
        """Prüft, ob ein Spielobjekt auf dem Board platziert werden kann.

        Kriterien:
        - Alle Zielzellen müssen innerhalb des Boards und frei sein.
        - Keine direkt angrenzende Zelle (inkl. Diagonalen) darf belegt sein.

        Args:
            obj (GameObject): Das zu platzierende Objekt mit gesetzten Koordinaten.
        Returns:
            bool: True, wenn Platzierung möglich ist, sonst False.
        """
        # Prüfe, ob alle Zellen frei sind
        for x, y in obj.coordinates:
            cell = self.get_cell(x, y)
            if not cell or cell.is_occupied:
                return False
        # Prüfe, ob angrenzende Zellen frei sind (keine direkten Nachbarn)
        for cell in self._get_adjacent_cells(obj):
            if cell.is_occupied:
                return False
        return True

    def place_object(self, obj: GameObject) -> bool:
        """Platziert ein Objekt auf dem Board, sofern die Platzierung gültig ist.

        Args:
            obj (GameObject): Das zu platzierende Objekt mit zuvor gesetzten Koordinaten.
        Returns:
            bool: True bei erfolgreicher Platzierung, sonst False.
        """
        if not self.can_place_object(obj):
            return False

        for x, y in obj.coordinates:
            self.get_cell(x, y).place_object(obj)

        obj.is_placed = True
        self.objects.append(obj)
        return True

    def remove_object(self, obj: GameObject):
        """Entfernt ein zuvor platziertes Objekt vom Board und bereinigt Zustand.

        Args:
            obj (GameObject): Das zu entfernende Objekt.
        """
        for x, y in obj.coordinates:
            cell = self.get_cell(x, y)
            if cell and cell.object == obj:
                cell.object = None

        obj.is_placed = False
        if obj in self.objects:
            self.objects.remove(obj)

    def _get_adjacent_cells(self, obj: GameObject) -> list[Cell]:
        """Ermittelt alle angrenzenden Zellen (inkl. Diagonalen) zu den Koordinaten eines Objekts.

        Args:
            obj (GameObject): Objekt, dessen Umgebung geprüft wird.
        Returns:
            list[Cell]: Liste der angrenzenden Zellen innerhalb der Board-Grenzen.
        """
        adjacent = set()

        for x, y in obj.coordinates:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    ax, ay = x + dx, y + dy
                    if (dx == 0 and dy == 0) or not (0 <= ax < self.width and 0 <= ay < self.height):
                        continue
                    adjacent.add(self.get_cell(ax, ay))

        return list(adjacent)

    def _clear_all_adjacent_markers(self):
        """Entfernt alle temporären Nachbar-Markierungen von sämtlichen Zellen."""
        for row in self.grid:
            for cell in row:
                cell.clear_adjacent()

    def _mark_adjacent_for_object(self, obj: GameObject):
        """Markiert freie, angrenzende Zellen rund um ein Objekt (z. B. für Hover-Vorschau)."""
        for cell in self._get_adjacent_cells(obj):
            if not cell.is_occupied:
                cell.mark_adjacent()

    def shoot_at(self, x: int, y: int) -> ShootResult:
        """Führt einen Schuss auf die Zelle (x, y) aus, sofern gültig.

        Args:
            x (int): Spaltenindex.
            y (int): Zeilenindex.
        Returns:
            bool: True bei Treffer, False bei Fehlschuss oder ungültiger Schuss.
        """
        cell = self.get_cell(x, y)
        if not cell or cell.is_shot:
            return ShootResult(False, False, cell is None)
        return cell.shoot()