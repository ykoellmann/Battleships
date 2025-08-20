from dataclasses import dataclass

from src.Core.Entities.GameObject import GameObject


@dataclass
class ShootResult:
    """
    Represents the result of shooting at a cell on the game board.
    
    Contains information about whether the shot was a hit or miss,
    whether the target was destroyed, and which object was hit.
    
    Attributes:
        hit: True if the shot hit an object, False otherwise
        is_destroyed: True if the hit object was destroyed, False otherwise
        missed: True if the shot missed (hit empty cell), False otherwise
        hit_object: The game object that was hit, None if missed
    """
    hit: bool
    is_destroyed: bool
    missed: bool
    hit_object: GameObject | None = None

    @staticmethod
    def miss():
        """
        Create a ShootResult representing a missed shot.
        
        Returns:
            ShootResult: Result indicating a miss (no hit, no destruction, missed=True)
        """
        return ShootResult(False, False, True)