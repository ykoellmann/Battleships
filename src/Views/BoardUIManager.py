from typing import List
from src.Utils.GameState import GameState
from src.Core.GamePhases.ExtendedShootingPhase import ExtendedShootingPhase
from src.Players.HumanPlayer import HumanPlayer
from src.Players.Computer.ComputerPlayer import ComputerPlayer
from src.Views.BoardView import BoardView
from src.Views.HoverManager import HoverManager


class BoardUIManager:
    """
    Manages board updates and state coordination for the game UI.
    
    This class handles all board-specific update operations,
    coordinating with HoverManager for highlighting effects
    and managing board enabling/disabling for different phases.
    
    Attributes:
        board_views: List of BoardView instances to manage
        hover_manager: HoverManager instance for hover state coordination
    """
    
    def __init__(self, board_views: List[BoardView], hover_manager: HoverManager):
        """
        Initialize the BoardUIManager with board views and hover manager.
        
        Args:
            board_views: List of BoardView instances to manage
            hover_manager: HoverManager for hover state coordination
        """
        self.board_views = board_views
        self.hover_manager = hover_manager
    
    def update_boards(self, game_phase) -> None:
        """
        Update all board views based on the current game state.
        
        Args:
            game_phase: Current game phase instance
        """
        # If current player is a computer, could add delay here if needed
        # For now, just proceed with internal updates
        if isinstance(game_phase.current_player, ComputerPlayer):
            # Computer turn handling - delay could be added here
            self._update_boards_internal(game_phase)
        else:
            self._update_boards_internal(game_phase)
    
    def _update_boards_internal(self, game_phase) -> None:
        """
        Internal method to dispatch board updates based on game state.
        
        Args:
            game_phase: Current game phase instance
        """
        if game_phase.state == GameState.Placement:
            self._update_boards_placement(game_phase)
        elif game_phase.state == GameState.Shooting:
            self._update_boards_shooting(game_phase)
        else:
            self._update_boards_pregame()
    
    def _update_boards_placement(self, game_phase) -> None:
        """
        Update boards for placement phase.
        
        Args:
            game_phase: Current placement phase instance
        """
        # Check if current player is human for hover enabling
        is_human_turn = isinstance(game_phase.current_player, HumanPlayer)
        
        for idx, board_view in enumerate(self.board_views):
            board_view.set_hover_enabled(is_human_turn)
            is_current_player = idx == game_phase.current_player_idx
            is_human_board = isinstance(game_phase.players[idx], HumanPlayer)
            
            # Determine visibility based on the new rules
            hide_ships_mines = HoverManager.should_hide_ships_mines(game_phase, idx)

            if is_current_player:
                # Update with current hover highlights
                hover_state = self.hover_manager.get_hover_state()
                board_view.update(
                    highlight_cells=hover_state['hover_cells'],
                    highlight_invalid_cells=hover_state['hover_invalid_cells'],
                    hide_ships_mines=hide_ships_mines
                )
                board_view.set_enabled(is_human_board)
            else:
                board_view.update(
                    hide_ships_mines=hide_ships_mines
                )
                board_view.set_enabled(False)
    
    def _update_boards_shooting(self, game_phase) -> None:
        """
        Update boards for shooting phase.
        
        Args:
            game_phase: Current shooting phase instance
        """
        is_human = isinstance(game_phase.current_player, HumanPlayer)

        for idx, board_view in enumerate(self.board_views):
            # Only enable hover if current player is human
            board_view.set_hover_enabled(is_human)
            
            is_current_player = idx == game_phase.current_player_idx
            is_human_board = isinstance(game_phase.players[idx], HumanPlayer)
            
            # Determine visibility based on the new rules
            hide_ships_mines = HoverManager.should_hide_ships_mines(game_phase, idx)
            
            # Handle extended shooting phase with ship highlighting
            if isinstance(game_phase, ExtendedShootingPhase):
                hover_state = self.hover_manager.get_hover_state()
                if idx == game_phase.current_player_idx:
                    # Current player board shows ship selection highlighting
                    board_view.update(
                        ship_hover_cells=hover_state['ship_hover_cells'],
                        ship_selected_cells=hover_state['ship_selected_cells'],
                        hide_ships_mines=hide_ships_mines
                    )
                else:
                    # Enemy board normal update
                    board_view.update(
                        hide_ships_mines=hide_ships_mines
                    )
            else:
                board_view.update(
                    hide_ships_mines=hide_ships_mines
                )

            # Enable enemy board for humans, or enable current player board for extended mode (only for humans)
            is_enemy_board = idx == 1 - game_phase.current_player_idx
            if isinstance(game_phase, ExtendedShootingPhase):
                # In extended mode, enable boards only for humans
                board_view.set_enabled(is_human)
            else:
                # In normal mode, only enable enemy board for humans
                board_view.set_enabled(is_enemy_board and is_human)
    
    def _update_boards_pregame(self) -> None:
        """Update boards for pre-game state."""
        for board_view in self.board_views:
            board_view.set_hover_enabled(False)
            board_view.update(hide_ships_mines=False)
            board_view.set_enabled(False)
    
    def update_board_at_index(self, board_idx: int, **update_args) -> None:
        """
        Update a specific board with given parameters.
        
        Args:
            board_idx: Index of the board to update
            **update_args: Arguments to pass to the board's update method
        """
        if 0 <= board_idx < len(self.board_views):
            self.board_views[board_idx].update(**update_args)
    
    def set_board_enabled(self, board_idx: int, enabled: bool) -> None:
        """
        Enable or disable a specific board.
        
        Args:
            board_idx: Index of the board to enable/disable
            enabled: True to enable, False to disable
        """
        if 0 <= board_idx < len(self.board_views):
            self.board_views[board_idx].set_enabled(enabled)
    
    def set_board_hover_enabled(self, board_idx: int, enabled: bool) -> None:
        """
        Enable or disable hover for a specific board.
        
        Args:
            board_idx: Index of the board
            enabled: True to enable hover, False to disable
        """
        if 0 <= board_idx < len(self.board_views):
            self.board_views[board_idx].set_hover_enabled(enabled)
    
    def enable_all_boards(self, enabled: bool) -> None:
        """
        Enable or disable all boards.
        
        Args:
            enabled: True to enable all boards, False to disable
        """
        for board_view in self.board_views:
            board_view.set_enabled(enabled)
    
    def set_hover_enabled_all_boards(self, enabled: bool) -> None:
        """
        Enable or disable hover for all boards.
        
        Args:
            enabled: True to enable hover, False to disable
        """
        for board_view in self.board_views:
            board_view.set_hover_enabled(enabled)
    
    def update_all_boards(self, **update_args) -> None:
        """
        Update all boards with the same parameters.
        
        Args:
            **update_args: Arguments to pass to each board's update method
        """
        for board_view in self.board_views:
            board_view.update(**update_args)
    
    def get_board_count(self) -> int:
        """
        Get the number of managed boards.
        
        Returns:
            Number of boards managed by this instance
        """
        return len(self.board_views)
    
    def get_board_view(self, board_idx: int) -> BoardView:
        """
        Get a specific board view by index.
        
        Args:
            board_idx: Index of the board to retrieve
            
        Returns:
            BoardView instance at the specified index
            
        Raises:
            IndexError: If board_idx is out of range
        """
        if 0 <= board_idx < len(self.board_views):
            return self.board_views[board_idx]
        raise IndexError(f"Board index {board_idx} out of range (0-{len(self.board_views)-1})")
    
    def refresh_all_boards(self, game_phase) -> None:
        """
        Force refresh all boards based on current game phase.
        
        Args:
            game_phase: Current game phase instance
        """
        self._update_boards_internal(game_phase)