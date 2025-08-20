import sqlite3
from typing import List, Dict, Tuple

from src.Utils.Database.Shot.UserShot import UserShot


class UserShotRepository:
    """
    Repository for user_shots table operations.

    Handles insert and select operations for user shot records,
    providing methods to store new shots and retrieve shooting statistics.

    Attributes:
        db_path: Path to the SQLite database file
    """

    def __init__(self, db_path: str):
        """
        Initialize the repository with database path.

        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path

    def insert(self, shot: UserShot) -> int:
        """
        Insert a new user shot record into the database.

        Args:
            shot: UserShot dataclass instance to insert

        Returns:
            int: The ID of the inserted record
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                           INSERT INTO user_shots (player_name, x, y, was_hit)
                           VALUES (?, ?, ?, ?)
                           """, (shot.player_name, shot.x, shot.y, shot.was_hit))
            conn.commit()
            return cursor.lastrowid

    def store_shot(self, player_name: str, x: int, y: int, was_hit: bool) -> int:
        """
        Store user shot in database (overloaded method).

        Args:
            player_name: Name of the player taking the shot
            x: X coordinate of the shot
            y: Y coordinate of the shot
            was_hit: Whether the shot was a hit

        Returns:
            int: The ID of the inserted record
        """
        shot = UserShot(
            player_name=player_name,
            x=x,
            y=y,
            was_hit=was_hit
        )
        return self.insert(shot)

    def get_shot_heatmap(self) -> Dict[Tuple[int, int], int]:
        """
        Get frequency map of where users typically shoot using direct SQL query.

        Returns:
            Dict[Tuple[int, int], int]: Dictionary mapping coordinates to frequency counts
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                           SELECT x, y, COUNT(*) as frequency
                           FROM user_shots
                           GROUP BY x, y
                           """)
            result = cursor.fetchall()

        return {(x, y): frequency for x, y, frequency in result}

    def get_shot_count(self) -> int:
        """
        Get total count of shot records.

        Returns:
            int: Total number of shot records
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM user_shots")
            return cursor.fetchone()[0]

    def clear_all(self):
        """Clear all shot records from the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM user_shots")
            conn.commit()