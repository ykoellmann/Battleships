"""
Database manager for storing and analyzing user behavior patterns.

This module provides SQLite integration for the Battleships game to store
user ship placements and shots for statistical analysis by the AI.
"""

import sqlite3
from typing import Dict

from src.Utils.Database.Placement.UserPlacementRepository import UserPlacementRepository
from src.Utils.Database.Shot.UserShotRepository import UserShotRepository


class DatabaseManager:
    """
    Manages SQLite database operations for storing and analyzing user behavior.
    
    Handles storage of user ship placements and shots, and provides
    statistical analysis for AI decision making based on user patterns.
    Uses repository classes for clean separation of concerns.
    
    Attributes:
        db_path: Path to the SQLite database file
        placement_repo: Repository for user placement operations
        shot_repo: Repository for user shot operations
    """
    
    def __init__(self, db_path: str = "battleships_data.db"):
        """
        Initialize database connection and create tables if needed.
        
        Args:
            db_path: Path to the SQLite database file (default: "battleships_data.db")
        """
        self.db_path = db_path
        self._init_database()
        self.placement_repo = UserPlacementRepository(db_path)
        self.shot_repo = UserShotRepository(db_path)
    
    def _init_database(self):
        """Initialize database with required tables (no heatmap tables - use direct SQL queries instead)."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabelle für Benutzer-Platzierungen
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_placements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_name TEXT NOT NULL,
                    ship_type TEXT NOT NULL,
                    x INTEGER NOT NULL,
                    y INTEGER NOT NULL,
                    orientation TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabelle für Benutzer-Schüsse
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_shots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_name TEXT NOT NULL,
                    x INTEGER NOT NULL,
                    y INTEGER NOT NULL,
                    was_hit BOOLEAN NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
    
    
    
    def clear_data(self):
        """Clear all stored user data (for testing/reset purposes)."""
        self.placement_repo.clear_all()
        self.shot_repo.clear_all()
    
    def get_statistics(self) -> Dict[str, int]:
        """
        Get basic statistics about stored data using repositories.
        
        Returns:
            Dict[str, int]: Dictionary with counts of placements and shots
        """
        return {
            'placements': self.placement_repo.get_placement_count(),
            'shots': self.shot_repo.get_shot_count()
        }