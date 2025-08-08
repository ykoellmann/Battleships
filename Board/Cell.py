from Objects.GameObject import GameObject


class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.object: GameObject | None = None  # Objekt, das diese Zelle belegt
        self.is_shot: bool = False             # Wurde auf diese Zelle geschossen?
        self.is_adjacent: bool = False         # Wird als angrenzend angezeigt (z. B. Hover-Vorschau)

    def place_object(self, obj: GameObject):
        self.object = obj

    def mark_adjacent(self):
        self.is_adjacent = True

    def clear_adjacent(self):
        self.is_adjacent = False

    def shoot(self):
        self.is_shot = True
        if self.object:
            self.object.on_hit(self.x, self.y)
            return True  # Treffer
        return False     # Fehlschuss

    def is_occupied(self) -> bool:
        return self.object is not None

    def is_hit(self) -> bool:
        return self.is_shot and self.object is not None

    def is_miss(self) -> bool:
        return self.is_shot and self.object is None

    def __repr__(self):
        return f"Cell({self.x}, {self.y}, occupied={self.is_occupied()}, shot={self.is_shot})"