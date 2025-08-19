import datetime
from typing import List, Optional
from dataclasses import dataclass
from src.Core.Entities.GameObject import GameObject
from src.Core.Entities.Ships.Ship import Ship
from src.Core.Entities.Mine import Mine


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


class GameLogger:
    """
    Central static logging system for game events.
    
    Captures and stores timestamped log entries for all game actions including
    ship placement, shooting, hits, misses, ship destruction, and mine explosions.
    
    All methods are static and can be called directly without instantiation.
    
    Class Attributes:
        _entries: List of all log entries in chronological order
    """
    
    _entries: List[LogEntry] = []
    
    @staticmethod
    def _add_entry(player_name: str, action: str, result: str):
        """
        Add a new log entry with current timestamp.
        
        Args:
            player_name: Name of the player performing the action
            action: Description of what action was performed
            result: Result or outcome of the action
        """
        entry = LogEntry(
            timestamp=datetime.datetime.now(),
            player_name=player_name,
            action=action,
            result=result
        )
        GameLogger._entries.append(entry)
    
    @staticmethod
    def log_ship_placement(player_name: str, ship: Ship, x: int, y: int, success: bool):
        """
        Log ship placement attempt.
        
        Args:
            player_name: Name of the player placing the ship
            ship: The ship being placed
            x: X coordinate of placement
            y: Y coordinate of placement  
            success: Whether the placement was successful
        """
        ship_name = ship.__class__.__name__
        action = f"platziert {ship_name} bei ({x},{y})"
        result = "erfolgreich" if success else "fehlgeschlagen"
        GameLogger._add_entry(player_name, action, result)
    
    @staticmethod
    def log_shot(player_name: str, x: int, y: int, hit: bool, hit_object: Optional[GameObject] = None, 
                 is_destroyed: bool = False):
        """
        Log shooting attempt and its result.
        
        Args:
            player_name: Name of the player shooting
            x: X coordinate of the shot
            y: Y coordinate of the shot
            hit: Whether the shot was a hit
            hit_object: The object that was hit (if any)
            is_destroyed: Whether the hit object was destroyed
        """
        action = f"schießt auf ({x},{y})"
        
        if not hit:
            result = "Fehlschuss"
        elif isinstance(hit_object, Ship):
            ship_name = hit_object.__class__.__name__
            if is_destroyed:
                result = f"trifft {ship_name} - Schiff zerstört"
            else:
                result = f"trifft {ship_name}"
        elif isinstance(hit_object, Mine):
            result = "trifft Mine - Explosion"
        else:
            result = "Treffer"
        
        GameLogger._add_entry(player_name, action, result)
    
    @staticmethod
    def log_mine_explosion(player_name: str, destroyed_ship: Ship):
        """
        Log when a player's own ship is destroyed by hitting a mine.
        
        Args:
            player_name: Name of the player whose ship was destroyed
            destroyed_ship: The ship that was destroyed by the mine
        """
        ship_name = destroyed_ship.__class__.__name__
        action = "Mine getroffen"
        result = f"eigenes Schiff {ship_name} zerstört"
        GameLogger._add_entry(player_name, action, result)
    
    @staticmethod
    def log_game_start(player1_name: str, player2_name: str):
        """
        Log the start of a new game.
        
        Args:
            player1_name: Name of the first player
            player2_name: Name of the second player
        """
        action = "Spiel gestartet"
        result = f"zwischen {player1_name} und {player2_name}"
        GameLogger._add_entry("System", action, result)
    
    @staticmethod
    def log_game_end(winner_name: str):
        """
        Log the end of a game.
        
        Args:
            winner_name: Name of the winning player
        """
        action = "Spiel beendet"
        result = f"Gewinner: {winner_name}"
        GameLogger._add_entry("System", action, result)
    
    @staticmethod
    def clear_log():
        """Clear all log entries."""
        GameLogger._entries.clear()
    
    @staticmethod
    def get_log_text() -> str:
        """
        Get all log entries as formatted text.
        
        Returns:
            str: All log entries formatted for display, one per line
        """
        return "\n".join(str(entry) for entry in GameLogger._entries)
    
    @staticmethod
    def get_recent_entries(count: int = 50) -> List[LogEntry]:
        """
        Get the most recent log entries.
        
        Args:
            count: Maximum number of entries to return
            
        Returns:
            List[LogEntry]: Most recent entries, newest first
        """
        return GameLogger._entries[-count:] if len(GameLogger._entries) > count else GameLogger._entries