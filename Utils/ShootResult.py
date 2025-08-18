from dataclasses import dataclass

from Objects.GameObject import GameObject


@dataclass
class ShootResult:
    hit: bool
    is_destroyed: bool
    missed: bool
    hit_object: GameObject | None = None

    @staticmethod
    def miss():
        return ShootResult(False, False, True)