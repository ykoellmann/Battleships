import sqlite3
from typing import List, Dict, Tuple

from src.Core.Entities.Ships.Ship import Ship
from src.Utils.Database.Placement.UserPlacement import UserPlacement


class UserPlacementRepository:
    """
    Repository for user_placements table operations.

    Handles insert and select operations for user ship placement records,
    providing methods to store new placements and retrieve placement statistics.

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

    def insert(self, placement: UserPlacement) -> int:
        """
        Insert a new user placement record into the database.

        Args:
            placement: UserPlacement dataclass instance to insert

        Returns:
            int: The ID of the inserted record
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                           INSERT INTO user_placements (player_name, ship_type, x, y, orientation)
                           VALUES (?, ?, ?, ?, ?)
                           """, (placement.player_name, placement.ship_type, placement.x, placement.y,
                                 placement.orientation))
            conn.commit()
            return cursor.lastrowid

    def store_placement(self, player_name: str, ship: Ship, x: int, y: int, orientation: str) -> int:
        """
        Store user ship placement in database (overloaded method).

        Args:
            player_name: Name of the player placing the ship
            ship: The ship being placed
            x: X coordinate of placement
            y: Y coordinate of placement
            orientation: Ship orientation as string

        Returns:
            int: The ID of the inserted record
        """
        placement = UserPlacement(
            player_name=player_name,
            ship_type=ship.__class__.__name__,
            x=x,
            y=y,
            orientation=orientation
        )
        return self.insert(placement)

    def select_all(self) -> List[UserPlacement]:
        """
        Select all user placement records from the database.

        Returns:
            List[UserPlacement]: List of all placement records
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                           SELECT id, player_name, ship_type, x, y, orientation, timestamp
                           FROM user_placements
                           ORDER BY timestamp DESC
                           """)
            results = cursor.fetchall()

        return [
            UserPlacement(
                id=row[0],
                player_name=row[1],
                ship_type=row[2],
                x=row[3],
                y=row[4],
                orientation=row[5],
                timestamp=row[6]
            )
            for row in results
        ]

    def get_placement_heatmap(self) -> Dict[Tuple[int, int], int]:
        """
        Get frequency map of where users typically place ships using direct SQL query.

        Returns:
            Dict[Tuple[int, int], int]: Dictionary mapping coordinates to frequency counts
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                           SELECT x, y, COUNT(*) as frequency
                           FROM user_placements
                           GROUP BY x, y
                           """)
            result = cursor.fetchall()

        return {(x, y): frequency for x, y, frequency in result}

    def get_placement_count(self) -> int:
        """
        Get total count of placement records.

        Returns:
            int: Total number of placement records
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM user_placements")
            return cursor.fetchone()[0]

    def clear_all(self):
        """Clear all placement records from the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM user_placements")
            conn.commit()