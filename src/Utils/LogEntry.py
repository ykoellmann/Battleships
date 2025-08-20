import datetime
from dataclasses import dataclass


@dataclass
class LogEntry:
    """
    Represents a single log entry with timestamp, player, action and result.

    Attributes:
        timestamp: When the action occurred
        player_name: Name of the player who performed the action
        action: Description of the action performed
        result: Result or outcome of the action
    """
    timestamp: datetime.datetime
    player_name: str
    action: str
    result: str

    def __str__(self) -> str:
        """Format log entry for display."""
        time_str = self.timestamp.strftime("%H:%M:%S")
        return f"[{time_str}] {self.player_name} - {self.action}: {self.result}"