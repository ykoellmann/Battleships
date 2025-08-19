import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class UserShot:
    """
    Represents a user shot record.

    Attributes:
        id: Primary key identifier (optional for inserts)
        player_name: Name of the player who took the shot
        x: X coordinate of the shot
        y: Y coordinate of the shot
        was_hit: Whether the shot resulted in a hit
        timestamp: When the shot occurred (optional, defaults to current time)
    """
    player_name: str
    x: int
    y: int
    was_hit: bool
    id: Optional[int] = None
    timestamp: Optional[datetime] = None