from enum import Enum


class GameState(Enum):
    """
    Enumeration of possible game states.
    
    Represents the current phase or state of the game to determine
    which actions are available and how the UI should behave.
    
    Values:
        End: Game has finished (winner determined)
        Placement: Players are placing their ships and mines
        Shooting: Players are taking turns shooting at each other
    """
    End = 1
    Placement = 2
    Shooting = 3