"""
Very Hard difficulty computer player with learning capabilities.

This module implements a computer player that learns from user behavior patterns
stored in a SQLite database to make more intelligent placement and targeting decisions.
"""

import random
from typing import List, Optional, Tuple, Dict
from src.Players.Computer.MediumComputerPlayer import MediumComputerPlayer
from src.Utils.Database.DatabaseManager import DatabaseManager
from src.Utils.Database.Placement.UserPlacementRepository import UserPlacementRepository
from src.Utils.Database.Shot.UserShotRepository import UserShotRepository
from src.Utils.Orientation import Orientation
from src.Core.Board.Board import Board


class HardComputerPlayer(MediumComputerPlayer):
    """
    Very Hard difficulty computer player that learns from user patterns.
    
    This computer player combines the intelligent hunting strategy of MediumComputerPlayer
    with statistical analysis of user behavior patterns for placement and targeting.
    It analyzes historical data to make predictions about where users are likely to
    place ships and where they typically shoot.
    
    Targeting Strategy:
    1. Intelligent hunting (inherited from MediumComputerPlayer)
    2. For random shots: Target areas where users place ships most frequently
    
    Placement Strategy:
    1. Avoid areas where users typically shoot
    2. Use areas where users place ships least frequently
    
    Attributes:
        name (str): Always "Schwer Computer"
        db_manager (DatabaseManager): Database manager for table initialization
        placement_repo (UserPlacementRepository): Repository for placement operations
        shot_repo (UserShotRepository): Repository for shot operations
        placement_heatmap (Dict): Frequency map of user ship placements
        shot_heatmap (Dict): Frequency map of user shots
    """
    
    def __init__(self, board: Board, db_manager: DatabaseManager):
        """
        Initialize VeryHardComputerPlayer with database access.
        
        Args:
            board: The player's game board instance
            db_manager: DatabaseManager instance for database initialization
        """
        super().__init__(board)
        self.name = "Schwerer Computer"
        self.db_manager = db_manager
        self.placement_repo = UserPlacementRepository(db_manager.db_path)
        self.shot_repo = UserShotRepository(db_manager.db_path)
        self.placement_heatmap = self.placement_repo.get_placement_heatmap()
        self.shot_heatmap = self.shot_repo.get_shot_heatmap()
        
    def select_target(self) -> Optional[Tuple[int, int]]:
        """
        Enhanced target selection using user behavior analysis.
        
        Priority order:
        1. Search queue (intelligent hunting - inherited from MediumComputerPlayer)
        2. Statistical targeting based on user placement patterns
        
        Returns:
            Optional[Tuple[int, int]]: The (x, y) coordinates of the selected target,
                                     or None if no targets are available
        """
        # First use the same intelligent hunting as HardComputerPlayer
        if self.search_queue:
            target = self.search_queue.pop(0)
            if target in self.available_targets:
                self.available_targets.remove(target)
                return target
            else:
                return self.select_target()
        
        # Enhanced statistical target selection
        if self.available_targets:
            return self._select_statistical_target()
        
        return None
    
    def _select_statistical_target(self) -> Tuple[int, int]:
        """
        Select target based on user placement patterns.
        
        Strategy: Target areas where users place ships most frequently,
        as this is where they're most likely to have ships.
        
        Returns:
            Tuple[int, int]: The (x, y) coordinates of the selected target
        """
        if not self.placement_heatmap:
            # Fallback: random selection if no data available
            target = random.choice(self.available_targets)
            self.available_targets.remove(target)
            return target
        
        # Create weighted target list based on user placement patterns
        weighted_targets = []
        for target in self.available_targets:
            frequency = self.placement_heatmap.get(target, 0)
            # Higher frequency = higher probability (minimum weight of 1)
            weight = max(1, frequency)
            weighted_targets.extend([target] * weight)
        
        target = random.choice(weighted_targets)
        self.available_targets.remove(target)
        return target
    
    def place_object(self, game_object) -> bool:
        """
        Enhanced placement strategy avoiding user shooting patterns.
        
        This method tries to place objects in areas where users shoot less frequently,
        making them harder to find. Falls back to standard placement if needed.
        
        Args:
            game_object: The game object to place
            
        Returns:
            bool: True if the object was successfully placed, False otherwise
        """
        if not self.shot_heatmap:
            # Fallback to parent class if no statistical data
            return super().place_object(game_object)
        
        # Try multiple placement attempts with statistical weighting
        best_positions = self._get_best_placement_positions(game_object)
        
        for position in best_positions:
            x, y, orientation = position
            game_object.x, game_object.y = x, y
            game_object.orientation = orientation
            if self.board.can_place_object(game_object):
                self.board.place_object(game_object)
                return True
        
        # Fallback: normal random placement
        return super().place_object(game_object)
    
    def _get_best_placement_positions(self, game_object) -> List[Tuple[int, int, Orientation]]:
        """
        Get placement positions sorted by desirability based on user shot patterns.
        
        Prefers areas where users shoot less frequently to make ships harder to find.
        
        Args:
            game_object: The game object to find positions for
            
        Returns:
            List[Tuple[int, int, Orientation]]: List of (x, y, orientation) tuples
                                                sorted by desirability
        """
        positions = []
        
        for x in range(self.board.width):
            for y in range(self.board.height):
                for orientation in [Orientation.HORIZONTAL, Orientation.VERTICAL]:
                    # Create temporary object to test placement
                    temp_obj = game_object.__class__()
                    temp_obj.x, temp_obj.y = x, y
                    temp_obj.orientation = orientation
                    
                    if self.board.can_place_object(temp_obj):
                        # Calculate position score based on user shot patterns
                        score = self._calculate_position_score(temp_obj)
                        positions.append((score, x, y, orientation))
        
        # Sort by score (lower values = less shot frequency = better)
        positions.sort(key=lambda x: x[0])
        return [(x, y, o) for _, x, y, o in positions[:10]]  # Return top 10 positions
    
    def _calculate_position_score(self, game_object) -> float:
        """
        Calculate desirability score for a placement position.
        
        Lower scores indicate better positions (less likely to be shot at).
        
        Args:
            game_object: The game object to calculate score for
            
        Returns:
            float: Average shot frequency for this position (lower is better)
        """
        total_shot_frequency = 0
        positions = game_object.get_positions()
        
        for pos in positions:
            frequency = self.shot_heatmap.get(pos, 0)
            total_shot_frequency += frequency
        
        # Return average shot frequency across all occupied positions
        return total_shot_frequency / len(positions) if positions else 0