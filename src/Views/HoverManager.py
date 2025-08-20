from typing import Set, Tuple, List

from src.Players.HumanPlayer import HumanPlayer
from src.Utils.GameState import GameState
from src.Core.GamePhases.ExtendedShootingPhase import ExtendedShootingPhase
from src.Views.BoardView import BoardView


class HoverManager:
    """
    Manages hover effects and highlighting for the game UI.
    
    This class provides centralized hover effect management for different
    game phases, including placement hover validation, ship selection
    highlighting, and dynamic cell highlighting updates.
    
    Attributes:
        board_views: List of BoardView instances for updating displays
        hover_cells: Set of coordinates with valid placement hover
        hover_invalid_cells: Set of coordinates with invalid placement hover
        ship_hover_cells: Set of coordinates with ship hover highlighting
        ship_selected_cells: Set of coordinates with selected ship highlighting
    """
    
    def __init__(self, board_views: List[BoardView]):
        """
        Initialize the HoverManager with board views for display updates.
        
        Args:
            board_views: List of BoardView instances to manage hover effects for
        """
        self.board_views = board_views
        self.hover_cells: Set[Tuple[int, int]] = set()
        self.hover_invalid_cells: Set[Tuple[int, int]] = set()
        self.ship_hover_cells: Set[Tuple[int, int]] = set()
        self.ship_selected_cells: Set[Tuple[int, int]] = set()
    
    def handle_cell_hover(self, x: int, y: int, enter: bool, player_idx: int, game_phase) -> None:
        """
        Handle cell hover events for different game phases.
        
        Args:
            x: Column index of the hovered cell
            y: Row index of the hovered cell
            enter: True when mouse enters cell, False when mouse leaves
            player_idx: Index of the player's board being hovered
            game_phase: Current game phase instance
        """
        # Handle placement phase hover
        if game_phase.state == GameState.Placement and self._is_hover_valid(player_idx, game_phase):
            if not enter:
                self.clear_hover_highlights(player_idx)
                return
            self._calculate_and_show_hover_highlights(x, y, player_idx, game_phase)
            return
        
        # Handle extended shooting phase ship hover
        if (game_phase.state == GameState.Shooting and 
            isinstance(game_phase, ExtendedShootingPhase) and
            player_idx == game_phase.current_player_idx):
            self._handle_ship_hover(x, y, enter, player_idx, game_phase)
    
    def _is_hover_valid(self, player_idx: int, game_phase) -> bool:
        """
        Check if hover is valid for the given player and game phase.
        
        Args:
            player_idx: Index of the player's board
            game_phase: Current game phase instance
            
        Returns:
            True if hover is valid, False otherwise
        """
        return (game_phase.state == GameState.Placement and
                player_idx == game_phase.current_player_idx)
    
    def clear_hover_highlights(self, player_idx: int) -> None:
        """
        Clear all hover highlights for a specific board.
        
        Args:
            player_idx: Index of the player's board to clear highlights for
        """
        self.hover_cells = set()
        self.hover_invalid_cells = set()
        if player_idx < len(self.board_views):
            self.board_views[player_idx].update()
    
    def _calculate_and_show_hover_highlights(self, x: int, y: int, player_idx: int, game_phase) -> None:
        """
        Calculate and display hover highlights for object placement.
        
        Args:
            x: Column index of the hovered cell
            y: Row index of the hovered cell
            player_idx: Index of the player's board
            game_phase: Current game phase instance
        """
        obj = game_phase.current_object
        obj.set_position(x, y)

        board = game_phase.players[player_idx].board
        highlight = set(obj.coordinates)

        if self._is_placement_valid(obj, board):
            self.hover_cells = highlight
            self.hover_invalid_cells = set()
        else:
            self.hover_cells = set()
            self.hover_invalid_cells = self._get_invalid_cells(obj, board, highlight)

        if player_idx < len(self.board_views):
            self.board_views[player_idx].update(
                highlight_cells=self.hover_cells,
                highlight_invalid_cells=self.hover_invalid_cells,
                hide_ships_mines=HoverManager.should_hide_ships_mines(game_phase, current_player_idx)
            )
    
    def _is_placement_valid(self, obj, board) -> bool:
        """
        Check if object placement is valid on the board.
        
        Args:
            obj: Game object to place
            board: Board to place object on
            
        Returns:
            True if placement is valid, False otherwise
        """
        return board.can_place_object(obj)
    
    def _get_invalid_cells(self, obj, board, highlight: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
        """
        Determine invalid cells for object placement.
        
        Args:
            obj: Game object to place
            board: Board to place object on
            highlight: Set of coordinates being highlighted
            
        Returns:
            Set of invalid cell coordinates
        """
        invalid_cells = set()
        for cx, cy in obj.coordinates:
            if not (0 <= cx < board.width and 0 <= cy < board.height):
                invalid_cells.add((cx, cy))

        # If object cannot be placed and no out-of-bounds cells, mark all as invalid
        if not board.can_place_object(obj) and not invalid_cells:
            invalid_cells = highlight

        return invalid_cells
    
    def _handle_ship_hover(self, x: int, y: int, enter: bool, player_idx: int, game_phase) -> None:
        """
        Handle ship hover effects in extended shooting phase.
        
        Args:
            x: Column index of the hovered cell
            y: Row index of the hovered cell
            enter: True when mouse enters cell, False when mouse leaves
            player_idx: Index of the player's board
            game_phase: Current game phase instance
        """
        if not enter:
            # Clear ship hover when leaving cell
            self.ship_hover_cells = set()
            # Preserve ship selection highlighting when clearing hover
            if player_idx < len(self.board_views):
                self.board_views[player_idx].update(
                    ship_hover_cells=self.ship_hover_cells,
                    ship_selected_cells=self.ship_selected_cells,
                    hide_ships_mines=HoverManager.should_hide_ships_mines(game_phase, player_idx)
                )
            return
        
        # Check if there's a ship at this position
        cell = game_phase.current_player.board.get_cell(x, y)
        if cell.object and cell.object.coordinates is not None:
            # Highlight all cells of the ship
            self.ship_hover_cells = set(cell.object.coordinates)
        else:
            self.ship_hover_cells = set()
        
        # Update with both hover and selection highlighting
        if player_idx < len(self.board_views):
            self.board_views[player_idx].update(
                ship_hover_cells=self.ship_hover_cells,
                ship_selected_cells=self.ship_selected_cells,
                hide_ships_mines=HoverManager.should_hide_ships_mines(game_phase, player_idx)
            )
    
    def update_ship_selection_highlighting(self, game_phase) -> None:
        """
        Update ship selection highlighting for extended shooting phase.
        
        Args:
            game_phase: Current game phase instance
        """
        if not isinstance(game_phase, ExtendedShootingPhase):
            return
        
        # Update selected ship highlighting - use active_ship if available, otherwise selected_ship
        active_ship = (game_phase.active_ship if game_phase.active_ship 
                       else game_phase.selected_ship)
        
        if active_ship:
            self.ship_selected_cells = set(active_ship.coordinates)
        else:
            self.ship_selected_cells = set()

            # Update the current player's board with selection highlighting
            current_player_idx = game_phase.current_player_idx
            if current_player_idx < len(self.board_views):
                self.board_views[current_player_idx].update(
                    ship_hover_cells=self.ship_hover_cells,
                    ship_selected_cells=self.ship_selected_cells,
                    hide_ships_mines=HoverManager.should_hide_ships_mines(game_phase, current_player_idx)
                )

    @staticmethod
    def should_hide_ships_mines(game_phase, board_idx: int) -> bool:
        """
        Determine if ships and mines should be hidden on the specified board.

        Implements three visibility scenarios:
        1. Computer vs Computer: No restrictions (show everything)
        2. Human vs Human: Hide ships/mines on opponent boards
        3. Human vs Computer: Always show human boards, always hide computer boards

        Args:
            game_phase: Current game phase instance
            board_idx: Index of the board to check

        Returns:
            bool: True if ships/mines should be hidden, False otherwise
        """
        player1_is_human = isinstance(game_phase.players[0], HumanPlayer)
        player2_is_human = isinstance(game_phase.players[1], HumanPlayer)
        current_board_is_human = isinstance(game_phase.players[board_idx], HumanPlayer)
        is_current_player_board = board_idx == game_phase.current_player_idx

        # Case 1: Computer vs Computer - show everything
        if not player1_is_human and not player2_is_human:
            return False

        # Case 2: Human vs Human - hide opponent ships/mines
        if player1_is_human and player2_is_human:
            return not is_current_player_board

        # Case 3: Human vs Computer - always show human boards, always hide computer boards
        if (player1_is_human and not player2_is_human) or (not player1_is_human and player2_is_human):
            return not current_board_is_human

        return False
    
    def clear_all_highlights(self) -> None:
        """Clear all hover and selection highlights from all boards."""
        self.hover_cells = set()
        self.hover_invalid_cells = set()
        self.ship_hover_cells = set()
        self.ship_selected_cells = set()
        
        for board_view in self.board_views:
            board_view.update(hide_ships_mines=False)
    
    def get_hover_state(self) -> dict:
        """
        Get current hover state for debugging or state management.
        
        Returns:
            Dictionary containing current hover state
        """
        return {
            'hover_cells': self.hover_cells.copy(),
            'hover_invalid_cells': self.hover_invalid_cells.copy(),
            'ship_hover_cells': self.ship_hover_cells.copy(),
            'ship_selected_cells': self.ship_selected_cells.copy()
        }