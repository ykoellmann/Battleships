import tkinter as tk
from tkinter import ttk, messagebox
from typing import Type

from src.Utils.Constants import (
    GameMode, UIConfig, UIColors,
    ButtonLabels, MessageConstants
)

from src.Core.Board.Board import Board
from src.Core.GamePhases.EndPhase import EndPhase
from src.Core.GamePhases.ExtendedPlacementPhase import ExtendedPlacementPhase
from src.Core.GamePhases.ExtendedShootingPhase import ExtendedShootingPhase
from src.Core.GamePhases.GamePhase import GamePhase
from src.Core.GamePhases.PhaseConfig import PhaseConfig
from src.Core.GamePhases.PlacementPhase import PlacementPhase
from src.Core.GamePhases.ShootingPhase import ShootingPhase
from src.Players.Computer.ComputerPlayer import ComputerPlayer
from src.Players.PlayerFactory import PlayerFactory
from src.Players.HumanPlayer import HumanPlayer

from src.Views.BoardView import BoardView
from src.Views.SettingsView import SettingsView, GameSettings
from src.Utils.GameLogger import GameLogger
from src.Views.LogWindow import LogWindow
from src.Views.ColorLegendWindow import ColorLegendWindow
from src.Views.StatisticsWindow import StatisticsWindow
from src.Utils.GameState import GameState

# Import the new manager classes
from src.Views.ButtonManager import ButtonManager
from src.Views.StyleManager import StyleManager
from src.Views.HoverManager import HoverManager
from src.Views.PhaseUIManager import PhaseUIManager
from src.Views.BoardUIManager import BoardUIManager


class GameUI:
    """
    Refactored UI layer for the game using specialized manager classes.
    
    This class coordinates between different UI managers to provide a clean,
    maintainable interface for the battleship game. Responsibilities are
    separated into specialized manager classes for better code organization.

    Attributes:
        window: Main tkinter window
        game_phase: Current game phase instance
        boards_frame: Frame containing game boards
        base_config: Base configuration for phase transitions
        winner: Winner of the game
        board_views: List of BoardView instances
        has_ended: Flag indicating if game has ended
        
        # Manager instances
        style_manager: Handles TTK styling configuration
        button_manager: Manages dynamic button creation and state
        hover_manager: Handles hover effects and highlighting
        phase_ui_manager: Coordinates phase-specific UI updates
        board_ui_manager: Manages board state and updates
        
        # UI Components
        settings_view: Game settings and start interface
        current_ship_label: Label showing current ship placement info
        button_frame: Frame containing game control buttons
        log_window: Game logging window
        color_legend_window: Color legend reference window
        statistics_window: Game statistics window
    """
    
    def __init__(self):
        """Initialize the GameUI with manager-based architecture."""
        self.window = tk.Tk()
        self.window.title("Schiffe Versenken")
        self.window.configure(bg=UIColors.WINDOW_BG)
        
        # Initialize style manager first (needed for other components)
        self.style_manager = StyleManager(self.window)
        
        # Initialize game state
        self.game_phase = None
        self.boards_frame = None
        self.base_config = None  # Base configuration to reuse for phase transitions
        self.winner = None  # Initialize winner instead of using hasattr
        self.has_ended = False

        # Initialize UI components
        self.settings_view = SettingsView(self.window, GameSettings(), self.start_game)
        self.settings_view.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

        # Current ship display label
        self.current_ship_label = ttk.Label(self.window, text="")
        self.current_ship_label.grid(row=2, column=0, columnspan=2, pady=5)

        # Create horizontal button frame below status text
        self.button_frame = tk.Frame(self.window, bg=UIColors.WINDOW_BG)
        self.button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        # Initialize button manager
        self.button_manager = ButtonManager(self.button_frame)

        # Create game boards
        self.board_views = []
        self.create_game_boards()

        # Initialize managers that depend on board_views
        self.hover_manager = HoverManager(self.board_views)
        self.phase_ui_manager = PhaseUIManager(self.current_ship_label, self.board_views, 
                                              self.button_manager, self.hover_manager)
        self.board_ui_manager = BoardUIManager(self.board_views, self.hover_manager)

        # Initialize auxiliary windows
        self.log_window = LogWindow(self.window)
        self.color_legend_window = ColorLegendWindow(self.window)
        self.statistics_window = StatisticsWindow(self.window)
        
        # Initialize database for AI learning
        GameLogger.initialize_database()
        
        # Create auxiliary buttons in SettingsView
        self.settings_view.create_log_button(self.log_window.open_window)
        self.settings_view.create_legend_button(self.color_legend_window.open_window)
        self.settings_view.create_statistics_button(self.statistics_window.open_window)

        

    def create_game_boards(self):
        boards_frame = ttk.Frame(self.window, padding=10, style='Brown.TFrame')
        boards_frame.grid(row=1, column=0, columnspan=2)

        self.boards_frame = boards_frame
        self.board_views.clear()
        for idx in range(2):
            frame = tk.LabelFrame(boards_frame, text=f"Spieler {idx+1}", 
                                 bg=UIColors.BOARD_FRAME_BG, fg=UIColors.BUTTON_FG,
                                 bd=2, relief="solid", padx=5, pady=5)
            frame.grid(row=0, column=idx, padx=10)
            board_view = BoardView(
                frame,
                click_callback=lambda x, y, p=idx: self.on_cell_click(x, y, p),
                hover_callback=lambda x, y, enter, p=idx: self.on_cell_hover(x, y, enter, p)
            )
            board_view.pack()
            # Hover im Pre-Game deaktiviert
            self.board_views.append(board_view)

    def start_game(self):
        # Cancel any pending timers from previous game
        if hasattr(self, 'game_phase') and self.game_phase:
            self.game_phase.cancel_all_timers()
        
        # Reset game state variables when starting a new game
        self.has_ended = False
        self.winner = None
        
        # Reset UI state variables through managers
        if hasattr(self, 'hover_manager'):
            self.hover_manager.clear_all_highlights()
        
        settings = self.settings_view.settings
        if settings.mode == GameMode.EXTENDED.value:
            game_phase_class = ExtendedPlacementPhase
        else:
            game_phase_class = PlacementPhase

        player1_board = Board()
        player2_board = Board()

        player1 = PlayerFactory.create(settings.p1_type, settings.p1_name, settings.p1_difficulty, player1_board, player2_board)
        player2 = PlayerFactory.create(settings.p2_type, settings.p2_name, settings.p2_difficulty, player2_board, player1_board)

        # Store base config for reuse in phase transitions
        self.base_config = PhaseConfig(
            state=GameState.Placement,
            player1=player1,
            player2=player2,
            turn_callback=self.placement_callback,
            next_phase_callback=self.next_phase_callback,  # Will be set later if needed
            settings=settings
        )
        self.game_phase = game_phase_class(self.base_config)
        self.game_phase.window = self.window  # Set window reference for timer management

        # Setze Boards in BoardViews
        for idx, board_view in enumerate(self.board_views):
            board_view.board = self.game_phase.players[idx].board
            board_view.update(hide_ships_mines=False)

        # Deactivate buttons through ButtonManager
        self.button_manager.toggle_button("auto_place", False, "", None)
        self.button_manager.toggle_button("orientation", False, "", None)
        
        # Log game start
        GameLogger.log_game_start(player1.name, player2.name)

        # Zentrale UI-Update statt verstreute Updates
        self.update_ui()
        self.game_phase.next_turn()

    def enable_placement_ui(self):
        """Enable UI elements specific to placement phase."""
        self.phase_ui_manager.enable_placement_ui(self.game_phase)

    def on_cell_click(self, x, y, player_idx):
        """Event-Handler für Klicks auf Zellen.

        Args:
            x (int): Spaltenindex der Zelle.
            y (int): Zeilenindex der Zelle.
            player_idx (int): Index des Boards (Spielers), auf dem geklickt wurde.
        """
        self.game_phase.handle_cell_click(x, y, player_idx == self.game_phase.current_player_idx)

        # UI-Update nach jeder Aktion
        self.update_ui()

    def shooting_callback(self):
        # Phase transitions are now handled by the phases themselves via next_phase_callback
        # No need to check is_over and create new phases here
        
        # Update log window if it's open
        self.log_window.update_log()
        
        # Zentrale UI-Update statt verstreute Updates
        self.update_ui()
        
        # Update boards to ensure visual changes are shown immediately (especially for computer turns)
        self.update_boards()

    def next_phase_callback(self, next_phase: Type[GamePhase]):
        match True:
            case _ if self.is_phase(next_phase, PlacementPhase):
                turn_callback = self.placement_callback
                state = GameState.Placement
            case _ if self.is_phase(next_phase, ShootingPhase):
                turn_callback = self.shooting_callback
                state = GameState.Shooting
                # Handle transition to shooting phase
                config = self.base_config.with_changes(
                    state=state,
                    turn_callback=turn_callback
                )
                self.game_phase = next_phase(config)
                self.game_phase.window = self.window
                self.start_real_game()
                return
            case _ if self.is_phase(next_phase, EndPhase):
                # Handle game end - set winner before creating EndPhase
                if not self.has_ended:
                    self.has_ended = True
                    self.winner = self.game_phase.current_player
                turn_callback = self._handle_game_end
                state = GameState.End
            case _:
                raise ValueError(f"Invalid phase transition: {next_phase}")

        config = self.base_config.with_changes(
            state = state,
            turn_callback=turn_callback
        )
        self.game_phase = next_phase(config)
        self.game_phase.next_turn()

        # Zentrale UI-Update statt verstreute Updates
        self.update_ui()

    def is_phase(self, next_phase: Type[GamePhase], check_type: Type[GamePhase]):
        return next_phase is check_type or issubclass(next_phase, check_type)

    def placement_callback(self, is_placed, is_over):
        if not is_placed:
            messagebox.showwarning(MessageConstants.INVALID_PLACEMENT, MessageConstants.INVALID_PLACEMENT_MESSAGE)
            return

        # Phase transitions are now handled by the phases themselves via next_phase_callback
        # No need to check is_over and create new phases here

        # Update log window if it's open
        self.log_window.update_log()

        # Zentrale UI-Update statt verstreute Updates
        self.update_ui()


    def _handle_game_end(self):
        # Log game end
        if self.winner:
            GameLogger.log_game_end(self.winner.name)
        
        messagebox.showinfo(MessageConstants.GAME_END, f"{self.winner.name} hat gewonnen!")
        self.phase_ui_manager.set_current_label_text(ButtonLabels.GAME_ENDED)
        return True

    def start_real_game(self):
        messagebox.showinfo(MessageConstants.GAME_START, MessageConstants.GAME_START_MESSAGE)
        # Zentrale UI-Update statt verstreute Updates
        self.update_ui()
        # Wenn der erste Spieler ein Computer ist, lass ihn sofort schießen
        self.game_phase.next_turn(True)

    def on_cell_hover(self, x, y, enter, player_idx):
        """Event handler for cell hover events, delegated to HoverManager."""
        self.hover_manager.handle_cell_hover(x, y, enter, player_idx, self.game_phase)

    def update_ui(self):
        """
        Central method for updating the entire UI based on the current game state.
        
        This method is delegated to the PhaseUIManager which coordinates all
        UI updates and ensures consistency with the current game state.
        """
        self.phase_ui_manager.update_ui(self.game_phase)

    def update_boards(self):
        """Update all board views based on the current game state, delegated to BoardUIManager."""
        self.board_ui_manager.update_boards(self.game_phase)

    def run(self):
        self.window.mainloop()
