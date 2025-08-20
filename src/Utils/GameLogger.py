import datetime
from typing import List, Optional
from dataclasses import dataclass
from src.Core.Entities.GameObject import GameObject
from src.Core.Entities.Ships.Ship import Ship
from src.Core.Entities.Mine import Mine
from src.Utils.Database.DatabaseManager import DatabaseManager
from src.Utils.Constants import ButtonLabels
from src.Utils.LogEntry import LogEntry


class GameLogger:
    """
    Central static logging system for game events.
    
    Captures and stores timestamped log entries for all game actions including
    ship placement, shooting, hits, misses, ship destruction, and mine explosions.
    Also stores user behavior data in SQLite database for AI learning.
    
    All methods are static and can be called directly without instantiation.
    
    Class Attributes:
        _entries: List of all log entries in chronological order
        _db_manager: DatabaseManager instance for persistent data storage
    """
    
    _entries: List[LogEntry] = []
    _db_manager: Optional[DatabaseManager] = None
    
    @staticmethod
    def initialize_database(db_path: str = None):
        """
        Initialize database connection for persistent logging.
        
        Args:
            db_path: Path to the SQLite database file (optional)
        """
        GameLogger._db_manager = DatabaseManager(db_path) if db_path else DatabaseManager()
    
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
        Log ship placement attempt and store in database for learning.
        
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
        
        # Store successful human player placements in database for AI learning
        if GameLogger._db_manager and success and not player_name.endswith("Computer"):
            GameLogger._db_manager.placement_repo.store_placement(player_name, ship, x, y, ship.orientation.name)
    
    @staticmethod
    def log_shot(player_name: str, x: int, y: int, hit: bool, hit_object: Optional[GameObject] = None, 
                 is_destroyed: bool = False):
        """
        Log shooting attempt and its result, storing in database for learning.
        
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
        
        # Store human player shots in database for AI learning
        if GameLogger._db_manager and not player_name.endswith("Computer"):
            GameLogger._db_manager.shot_repo.store_shot(player_name, x, y, hit)
    
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
        action = ButtonLabels.GAME_ENDED
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