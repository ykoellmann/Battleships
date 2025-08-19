import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class UserPlacement:
    """
    Represents a user ship placement record.

    Attributes:
        id: Primary key identifier (optional for inserts)
        player_name: Name of the player who placed the ship
        ship_type: Type/class name of the ship placed
        x: X coordinate of the placement
        y: Y coordinate of the placement
        orientation: Orientation of the ship (HORIZONTAL/VERTICAL)
        timestamp: When the placement occurred (optional, defaults to current time)
    """
    player_name: str
    ship_type: str
    x: int
    y: int
    orientation: str
    id: Optional[int] = None
    timestamp: Optional[datetime] = None