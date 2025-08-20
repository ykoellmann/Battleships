"""
Phase-specific UI management for the GameUI class.

This module provides centralized UI update functionality for different
game phases, coordinating between various UI managers and components
to maintain consistent state throughout the game.
"""

import tkinter as tk
from tkinter import ttk
from typing import List
from src.Utils.GameState import GameState
from src.Core.GamePhases.ExtendedShootingPhase import ExtendedShootingPhase
from src.Players.HumanPlayer import HumanPlayer
from src.Views.BoardView import BoardView
from src.Views.ButtonManager import ButtonManager
from src.Views.HoverManager import HoverManager
from src.Utils.Constants import ButtonLabels, MessageConstants, ButtonType, UIColors


class PhaseUIManager:
    """
    Manages phase-specific UI updates for the game interface.
    
    This class coordinates UI updates across different game phases,
    working with other managers to ensure consistent state and
    proper UI configuration for each phase.
    
    Attributes:
        current_ship_label: Label widget showing current ship placement info
        board_views: List of BoardView instances for display updates
        button_manager: ButtonManager instance for button control
        hover_manager: HoverManager instance for hover effects
    """
    
    def __init__(self, current_ship_label: ttk.Label, board_views: List[BoardView], 
                 button_manager: ButtonManager, hover_manager: HoverManager):
        """
        Initialize the PhaseUIManager with UI components and managers.
        
        Args:
            current_ship_label: Label widget for current ship information
            board_views: List of BoardView instances to manage
            button_manager: ButtonManager for button control
            hover_manager: HoverManager for hover effects
        """
        self.current_ship_label = current_ship_label
        self.board_views = board_views
        self.button_manager = button_manager
        self.hover_manager = hover_manager
        self.selected_ship_label = None  # Label for showing selected ship in extended shooting phase
    
    def update_ui(self, game_phase) -> None:
        """
        Central method for updating the entire UI based on the current game state.
        
        This method unifies all UI updates and ensures the user interface
        is consistent with the current game state.
        
        Args:
            game_phase: Current game phase instance, None for pre-game
        """
        if not game_phase:
            self._update_ui_pregame()
            return

        match game_phase.state:
            case GameState.Placement:
                self._update_ui_placement(game_phase)
            case GameState.Shooting:
                self._update_ui_shooting(game_phase)
            case GameState.End:
                self._update_ui_end()
            case _:
                self._update_ui_pregame()
    
    def _update_ui_placement(self, game_phase) -> None:
        """
        UI updates for the placement phase.
        
        Args:
            game_phase: Current placement phase instance
        """
        # Label updates
        self.update_current_ship_label(game_phase)
        
        # Hide ship selection label (only for shooting phase)
        self._hide_selected_ship_label()
        
        # Button updates - only enable if current player is human
        is_human_turn = isinstance(game_phase.current_player, HumanPlayer)
        self.button_manager.toggle_button("orientation", is_human_turn, 
                                         ButtonLabels.TOGGLE_ORIENTATION, 
                                         lambda: game_phase.toggle_orientation())
        self.button_manager.toggle_button("auto_place", is_human_turn,
                                         ButtonLabels.AUTO_PLACE_ALL,
                                         lambda: self._handle_auto_place(game_phase))
        
        # Hover state - only enable if current player is human
        for board_view in self.board_views:
            board_view.set_hover_enabled(is_human_turn)
    
    def _update_ui_shooting(self, game_phase) -> None:
        """
        UI updates for the shooting phase.
        
        Args:
            game_phase: Current shooting phase instance
        """
        # Label updates (current player)
        if game_phase.current_player is not None:
            self.current_ship_label.config(text=f"{game_phase.current_player.name} ist am Zug")
        
        # Check if current player is human
        is_human_turn = isinstance(game_phase.current_player, HumanPlayer)
        
        # Button updates - different for Extended and Normal Mode, only enable for humans
        if isinstance(game_phase, ExtendedShootingPhase):
            # Create ship selection label if it doesn't exist
            self._create_selected_ship_label()
            # Update ship selection label text
            self._update_selected_ship_label(game_phase)
            
            # Check if selection is already confirmed (disable button if confirmed)
            button_enabled = is_human_turn and not game_phase.selection_done
            if button_enabled:
                self.button_manager.show_button_group(ButtonType.CONFIRMATION.value, 
                                                     confirmation=lambda: self._handle_ship_confirmation(game_phase))
            else:
                # Show button but keep it disabled
                self.button_manager.show_button_group(ButtonType.CONFIRMATION.value, 
                                                     confirmation=lambda: None)
                # Disable the confirmation button
                confirm_button = self.button_manager.get_button("confirmation")
                if confirm_button:
                    confirm_button.config(state="disabled")
            
            # Update selected ship highlighting
            self.hover_manager.update_ship_selection_highlighting(game_phase)
        else:
            # Hide ship selection label for normal mode
            self._hide_selected_ship_label()
            self.button_manager.show_button_group(ButtonType.NONE.value)
        
        # Hide placement-specific buttons
        self.button_manager.toggle_button("auto_place", False, "", None)
        self.button_manager.toggle_button("orientation", False, "", None)

        # Hover state - only enable if current player is human
        for board_view in self.board_views:
            board_view.set_hover_enabled(is_human_turn)
    
    def _update_ui_end(self) -> None:
        """UI updates for game end."""
        # Disable all boards
        for board_view in self.board_views:
            board_view.set_enabled(False)
            board_view.set_hover_enabled(False)
            board_view.update(hide_ships_mines=False)
        
        # Label updates
        self.current_ship_label.config(text=ButtonLabels.GAME_ENDED)
        
        # Hide ship selection label
        self._hide_selected_ship_label()
        
        # Button updates
        self.button_manager.toggle_button("orientation", False, "", None)
        self.button_manager.toggle_button("auto_place", False, "", None)
    
    def _update_ui_pregame(self) -> None:
        """UI updates for pre-game state."""
        for board_view in self.board_views:
            board_view.set_hover_enabled(False)
            board_view.update(hide_ships_mines=False)
            board_view.set_enabled(False)
        
        self.current_ship_label.config(text="")
        
        # Hide ship selection label
        self._hide_selected_ship_label()
        
        self.button_manager.toggle_button("orientation", False, "", None)
        self.button_manager.toggle_button("auto_place", False, "", None)
    
    def update_current_ship_label(self, game_phase) -> None:
        """
        Update the current ship placement label.
        
        Args:
            game_phase: Current game phase instance
        """
        if game_phase.state != GameState.Placement:
            self.current_ship_label.config(text="")
            return

        self.current_ship_label.config(
            text=f"{game_phase.current_player.name}: Platziere {str(game_phase.current_object)}"
        )
    
    def enable_placement_ui(self, game_phase) -> None:
        """
        Enable UI elements specific to placement phase.
        
        Args:
            game_phase: Current placement phase instance
        """
        # Check if current player is human
        is_human_turn = isinstance(game_phase.current_player, HumanPlayer)
        
        # Only the current player's board is active (own field)
        for idx, board_view in enumerate(self.board_views):
            if idx == game_phase.current_player_idx:
                board_view.set_enabled(is_human_turn)
            else:
                board_view.set_enabled(False)

        # Only enable buttons if current player is human
        self.button_manager.toggle_button("orientation", is_human_turn,
                                         ButtonLabels.TOGGLE_ORIENTATION,
                                         lambda: game_phase.toggle_orientation())
    
    def _handle_auto_place(self, game_phase) -> None:
        """
        Handle auto-placement button callback.
        
        Args:
            game_phase: Current placement phase instance
        """
        from tkinter import messagebox
        from src.Core.GamePhases.PlacementPhase import PlacementPhase
        
        if game_phase.state != GameState.Placement:
            return
        
        if isinstance(game_phase, PlacementPhase):
            success = game_phase.auto_place_all_ships()
            if success:
                # Ships were successfully placed, trigger next turn to handle phase transition
                game_phase.next_turn()
                # Note: UI update should be called from the main GameUI class after this
            else:
                messagebox.showwarning(MessageConstants.AUTO_PLACE_FAILED, 
                                     MessageConstants.AUTO_PLACE_FAILED_MESSAGE)
    
    def get_current_label_text(self) -> str:
        """
        Get the current text of the ship label.
        
        Returns:
            Current label text
        """
        return self.current_ship_label.cget("text")
    
    def set_current_label_text(self, text: str) -> None:
        """
        Set the text of the ship label.
        
        Args:
            text: Text to display in the label
        """
        self.current_ship_label.config(text=text)
    
    def disable_all_boards(self) -> None:
        """Disable all board interactions."""
        for board_view in self.board_views:
            board_view.set_enabled(False)
            board_view.set_hover_enabled(False)
    
    def enable_board(self, board_idx: int, enabled: bool = True) -> None:
        """
        Enable or disable a specific board.
        
        Args:
            board_idx: Index of the board to enable/disable
            enabled: True to enable, False to disable
        """
        if 0 <= board_idx < len(self.board_views):
            self.board_views[board_idx].set_enabled(enabled)
    
    def set_hover_for_all_boards(self, enabled: bool) -> None:
        """
        Enable or disable hover for all boards.
        
        Args:
            enabled: True to enable hover, False to disable
        """
        for board_view in self.board_views:
            board_view.set_hover_enabled(enabled)
    
    def _create_selected_ship_label(self) -> None:
        """Create the ship selection label if it doesn't exist."""
        if self.selected_ship_label is None:
            import tkinter as tk
            # Get the button frame from the button manager
            button_frame = self.button_manager.button_frame
            self.selected_ship_label = tk.Label(
                button_frame,
                text="Ausgewähltes Schiff: Kein Schiff",
                bg=UIColors.WINDOW_BG,
                fg=UIColors.BUTTON_FG
            )
            self.selected_ship_label.pack(side=tk.LEFT, padx=10)
    
    def _update_selected_ship_label(self, game_phase) -> None:
        """Update the ship selection label text based on current selection."""
        if self.selected_ship_label is None:
            return
            
        # Determine which ship is selected (active_ship for confirmed, selected_ship for temporary)
        selected_ship = game_phase.active_ship if game_phase.active_ship else game_phase.selected_ship
        
        if selected_ship:
            ship_name = selected_ship.__class__.__name__
            self.selected_ship_label.config(text=f"Ausgewähltes Schiff: {ship_name}")
        else:
            self.selected_ship_label.config(text="Ausgewähltes Schiff: Kein Schiff")
    
    def _hide_selected_ship_label(self) -> None:
        """Hide and destroy the ship selection label."""
        if self.selected_ship_label is not None:
            self.selected_ship_label.destroy()
            self.selected_ship_label = None
    
    def _handle_ship_confirmation(self, game_phase) -> None:
        """Handle ship selection confirmation and disable the button."""
        game_phase.confirm_ship_selection()
        # Update the label after confirmation
        self._update_selected_ship_label(game_phase)