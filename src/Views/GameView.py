import tkinter as tk
from tkinter import ttk, messagebox
from typing import Type

from src.Utils.constants import (
    GameMode, UIConfig, UIColors,
    ButtonLabels
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
from src.Utils.GameState import GameState


class GameUI:
    """
    UI-Schicht für das Spiel (Tkinter). Verwaltet die Anzeige der Spielfelder,
    die Platzierungsphase, die Schussphase und die Nutzerinteraktionen.

    Attribute:
        window: Tk-Hauptfenster.
        game (Game | None): Aktuelles Spiel.
        settings_view (SettingsView): Einstellungen/Startansicht mit Callback.
        current_ship_label: Label zur Anzeige des aktuellen zu platzierenden Objekts.
        board_views (list[BoardView]): UI-Ansichten für beide Spieler-Boards.
        hover_cells (set[tuple[int,int]]): Aktuelle Hover-Markierungen gültiger Zellen.
        hover_invalid_cells (set[tuple[int,int]]): Aktuelle Hover-Markierungen ungültiger Zellen.
    """
    COMPUTER_TURN_DELAY = 1  # Sekunden
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Schiffe Versenken")
        self.window.configure(bg=UIColors.WINDOW_BG)
        
        # Configure TTK styles for brownish theme
        self._configure_ttk_styles()
        self.game_phase = None
        self.boards_frame = None
        self.base_config = None  # Base configuration to reuse for phase transitions
        self.winner = None  # Initialize winner instead of using hasattr

        self.settings_view = SettingsView(self.window, GameSettings(), self.start_game)
        self.settings_view.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

        # Anzeige aktuelles Schiff
        self.current_ship_label = ttk.Label(self.window, text="")
        self.current_ship_label.grid(row=2, column=0, columnspan=2, pady=5)

        # Create horizontal button frame below status text
        self.button_frame = tk.Frame(self.window, bg=UIColors.WINDOW_BG)
        self.button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        # Initialize buttons as None instead of using hasattr
        self.orientation_button = None
        self.confirmation_button = None
        self.auto_place_button = None

        # Spielfelder
        self.board_views = []
        self.create_game_boards()
        self.has_ended = False

        self.hover_cells = set()
        self.ship_hover_cells = set()
        self.ship_selected_cells = set()
        self.hover_invalid_cells = set()

        # Initialize logging system (static class, no instantiation needed)
        self.log_window = LogWindow(self.window)
        
        # Initialize color legend window
        self.color_legend_window = ColorLegendWindow(self.window)
        
        # Log window button
        self.log_button = None
        
        # Color legend button
        self.legend_button = None

    def _configure_ttk_styles(self):
        """Configure TTK styles for brownish theme."""
        style = ttk.Style()
        
        # Set theme to default to ensure proper styling base
        style.theme_use('default')
        
        # Brown button style
        style.configure('Brown.TButton',
                        background=UIColors.BUTTON_BG,
                        foreground=UIColors.BUTTON_FG,
                        borderwidth=1,
                        focuscolor='none')
        style.map('Brown.TButton',
                  background=[('active', UIColors.BUTTON_ACTIVE_BG),
                             ('pressed', UIColors.BUTTON_ACTIVE_BG)])
        
        # Brown combobox style with aggressive configuration
        style.configure('Brown.TCombobox',
                        fieldbackground=UIColors.BUTTON_BG,
                        background=UIColors.BUTTON_BG,
                        foreground=UIColors.BUTTON_FG,
                        borderwidth=1,
                        arrowcolor=UIColors.BUTTON_FG,
                        insertcolor=UIColors.BUTTON_FG,
                        relief='flat',
                        lightcolor=UIColors.BUTTON_BG,
                        darkcolor=UIColors.BUTTON_BG)
        style.map('Brown.TCombobox',
                  fieldbackground=[('readonly', UIColors.BUTTON_BG),
                                 ('focus', UIColors.BUTTON_BG),
                                 ('!focus', UIColors.BUTTON_BG),
                                 ('active', UIColors.BUTTON_BG),
                                 ('!active', UIColors.BUTTON_BG)],
                  background=[('readonly', UIColors.BUTTON_BG),
                            ('focus', UIColors.BUTTON_BG),
                            ('!focus', UIColors.BUTTON_BG),
                            ('active', UIColors.BUTTON_BG),
                            ('!active', UIColors.BUTTON_BG)],
                  foreground=[('readonly', UIColors.BUTTON_FG),
                            ('focus', UIColors.BUTTON_FG),
                            ('!focus', UIColors.BUTTON_FG)],
                  selectbackground=[('readonly', UIColors.BUTTON_ACTIVE_BG)],
                  selectforeground=[('readonly', UIColors.BUTTON_FG)],
                  arrowcolor=[('readonly', UIColors.BUTTON_FG),
                            ('focus', UIColors.BUTTON_FG),
                            ('!focus', UIColors.BUTTON_FG)])
        
        # Configure combobox sub-elements more aggressively
        style.element_create('Brown.TCombobox.field', 'from', 'default')
        style.element_create('Brown.TCombobox.downarrow', 'from', 'default')
        
        # Layout configuration
        style.layout('Brown.TCombobox', [
            ('Brown.TCombobox.field', {'sticky': 'nswe', 'children': [
                ('Brown.TCombobox.padding', {'expand': '1', 'sticky': 'nswe', 'children': [
                    ('Brown.TCombobox.textarea', {'sticky': 'nswe'})
                ]})
            ]}),
            ('Brown.TCombobox.downarrow', {'side': 'right', 'sticky': 'ns'})
        ])
        
        # Configure individual elements
        style.configure('Brown.TCombobox.field',
                        background=UIColors.BUTTON_BG,
                        fieldbackground=UIColors.BUTTON_BG,
                        bordercolor=UIColors.BUTTON_ACTIVE_BG,
                        lightcolor=UIColors.BUTTON_BG,
                        darkcolor=UIColors.BUTTON_BG)
        
        style.configure('Brown.TCombobox.downarrow',
                        background=UIColors.BUTTON_BG,
                        arrowcolor=UIColors.BUTTON_FG)
        
        # Configure combobox Entry sub-element specifically
        style.configure('Brown.TCombobox.Entry',
                        background=UIColors.BUTTON_BG,
                        fieldbackground=UIColors.BUTTON_BG,
                        foreground=UIColors.BUTTON_FG,
                        insertcolor=UIColors.BUTTON_FG)
        style.map('Brown.TCombobox.Entry',
                  background=[('readonly', UIColors.BUTTON_BG),
                            ('focus', UIColors.BUTTON_BG),
                            ('!focus', UIColors.BUTTON_BG)],
                  fieldbackground=[('readonly', UIColors.BUTTON_BG),
                                 ('focus', UIColors.BUTTON_BG),
                                 ('!focus', UIColors.BUTTON_BG)],
                  foreground=[('readonly', UIColors.BUTTON_FG),
                            ('focus', UIColors.BUTTON_FG),
                            ('!focus', UIColors.BUTTON_FG)])
        
        # Configure combobox listbox (dropdown list)
        style.configure('Brown.TCombobox.Listbox',
                        background=UIColors.BUTTON_BG,
                        foreground=UIColors.BUTTON_FG,
                        selectbackground=UIColors.BUTTON_ACTIVE_BG,
                        selectforeground=UIColors.BUTTON_FG,
                        borderwidth=1)
        
        # Configure the dropdown window with more options
        self.window.option_add('*TCombobox*Listbox.Background', UIColors.BUTTON_BG)
        self.window.option_add('*TCombobox*Listbox.Foreground', UIColors.BUTTON_FG)
        self.window.option_add('*TCombobox*Listbox.selectBackground', UIColors.BUTTON_ACTIVE_BG)
        self.window.option_add('*TCombobox*Listbox.selectForeground', UIColors.BUTTON_FG)
        
        # Additional global combobox options
        self.window.option_add('*TCombobox*Entry.Background', UIColors.BUTTON_BG)
        self.window.option_add('*TCombobox*Entry.Foreground', UIColors.BUTTON_FG)
        self.window.option_add('*TCombobox.Background', UIColors.BUTTON_BG)
        self.window.option_add('*TCombobox.Foreground', UIColors.BUTTON_FG)
        
        # Brown frame style for boards container
        style.configure('Brown.TFrame',
                        background=UIColors.FRAME_BG)
        

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
        # Reset game state variables when starting a new game
        self.has_ended = False
        self.winner = None
        
        # Reset UI state variables
        self.hover_cells = set()
        self.ship_hover_cells = set()
        self.ship_selected_cells = set()
        
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

        # Setze Boards in BoardViews
        for idx, board_view in enumerate(self.board_views):
            board_view.board = self.game_phase.players[idx].board
            board_view.update()

        # Create log button
        self._create_log_button()
        
        # Create color legend button
        self._create_legend_button()
        
        # Log game start
        GameLogger.log_game_start(player1.name, player2.name)

        # Zentrale UI-Update statt verstreute Updates
        self.update_ui()
        self.game_phase.next_turn()

    def enable_placement_ui(self):
        # Nur das Board des aktuellen Spielers ist aktiv (eigenes Feld)
        for idx, board_view in enumerate(self.board_views):
            if idx == self.game_phase.current_player_idx:
                board_view.set_enabled(True)
            else:
                board_view.set_enabled(False)

        self._toggle_orientation_button(True)

    def _toggle_orientation_button(self, enabled: bool):
        """Stellt sicher, dass der Orientierungsbutton existiert und aktiviert ihn."""
        if self.orientation_button is None:
            self.orientation_button = tk.Button(
                self.button_frame,
                text=ButtonLabels.TOGGLE_ORIENTATION,
                command=lambda: self.game_phase.toggle_orientation(),
                bg=UIColors.BUTTON_BG,
                fg=UIColors.BUTTON_FG,
                activebackground=UIColors.BUTTON_ACTIVE_BG
            )
            self.orientation_button.pack(side=tk.LEFT, padx=5)

        state = "normal" if enabled else "disabled"
        self.orientation_button.config(state=state)

    def _toggle_confirmation_button(self, enabled: bool):
        """Stellt sicher, dass der Bestätigungsbutton für Schiffauswahl existiert und aktiviert ihn."""
        if self.confirmation_button is None:
            self.confirmation_button = tk.Button(
                self.button_frame,
                text=ButtonLabels.CONFIRM_SELECTION,
                command=lambda: self.game_phase.confirm_ship_selection(),
                bg=UIColors.BUTTON_BG,
                fg=UIColors.BUTTON_FG,
                activebackground=UIColors.BUTTON_ACTIVE_BG
            )
            self.confirmation_button.pack(side=tk.LEFT, padx=5)

        state = "normal" if enabled else "disabled"
        self.confirmation_button.config(state=state)

    def _toggle_auto_place_button(self, enabled: bool):
        """Stellt sicher, dass der Auto-Platzierungsbutton existiert und aktiviert ihn."""
        if self.auto_place_button is None:
            self.auto_place_button = tk.Button(
                self.button_frame,
                text=ButtonLabels.AUTO_PLACE_ALL,
                command=self._auto_place_all_ships,
                bg=UIColors.BUTTON_BG,
                fg=UIColors.BUTTON_FG,
                activebackground=UIColors.BUTTON_ACTIVE_BG
            )
            self.auto_place_button.pack(side=tk.LEFT, padx=5)

        state = "normal" if enabled else "disabled"
        self.auto_place_button.config(state=state)
    
    def _create_log_button(self):
        """Creates the log window button if it doesn't exist."""
        if self.log_button is None:
            self.log_button = tk.Button(
                self.button_frame,
                text="Spiel-Log öffnen",
                command=self.log_window.open_window,
                bg=UIColors.BUTTON_BG,
                fg=UIColors.BUTTON_FG,
                activebackground=UIColors.BUTTON_ACTIVE_BG
            )
            self.log_button.pack(side=tk.LEFT, padx=5)
    
    def _create_legend_button(self):
        """Creates the color legend button if it doesn't exist."""
        if self.legend_button is None:
            self.legend_button = tk.Button(
                self.button_frame,
                text="Farblegende",
                command=self.color_legend_window.open_window,
                bg=UIColors.BUTTON_BG,
                fg=UIColors.BUTTON_FG,
                activebackground=UIColors.BUTTON_ACTIVE_BG
            )
            self.legend_button.pack(side=tk.LEFT, padx=5)

    def _show_button(self, button_type: str):
        """Zeigt den entsprechenden Button an und versteckt den anderen."""
        if button_type == "orientation":
            if self.confirmation_button is not None:
                self.confirmation_button.grid_remove()
                self.confirmation_button = None
            self._toggle_orientation_button(True)
        elif button_type == "confirmation":
            if self.orientation_button is not None:
                self.orientation_button.grid_remove()
                self.orientation_button = None
            self._toggle_confirmation_button(True)
        elif button_type == "none":
            if self.orientation_button is not None:
                self.orientation_button.grid_remove()
                self.orientation_button = None
            if self.confirmation_button is not None:
                self.confirmation_button.grid_remove()
                self.confirmation_button = None


    def _auto_place_all_ships(self):
        """Callback für den Auto-Platzierungsbutton."""
        if self.game_phase.state != GameState.Placement:
            return
        
        if isinstance(self.game_phase, PlacementPhase):
            success = self.game_phase.auto_place_all_ships()
            if success:
                # Ships were successfully placed, trigger next turn to handle phase transition
                self.game_phase.next_turn()
                self.update_ui()
            else:
                messagebox.showwarning("Auto-Platzierung fehlgeschlagen", 
                                     "Nicht alle Schiffe konnten automatisch platziert werden!")

    def update_current_ship_label(self):
        if self.game_phase.state != GameState.Placement:
            self.current_ship_label.config(text="")
            return

        self.current_ship_label.config(text=f"{self.game_phase.current_player.name}: Platziere {str(self.game_phase.current_object)}]")

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

    def shooting_callback(self, hit, is_over):
        # Phase transitions are now handled by the phases themselves via next_phase_callback
        # No need to check is_over and create new phases here
        
        # Update log window if it's open
        self.log_window.update_log()
        
        # Zentrale UI-Update statt verstreute Updates
        self.update_ui()

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
            messagebox.showwarning("Ungültige Platzierung", "Hier kann das Schiff nicht platziert werden!")
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
        
        messagebox.showinfo("Spielende", f"{self.winner.name} hat gewonnen!")
        self.current_ship_label.config(text="Spiel beendet")
        return True

    def start_real_game(self):
        messagebox.showinfo("Spielstart", "Alle Schiffe platziert! Das Spiel beginnt.")
        # Zentrale UI-Update statt verstreute Updates
        self.update_ui()
        # Wenn der erste Spieler ein Computer ist, lass ihn sofort schießen
        self.game_phase.next_turn(True)

    def on_cell_hover(self, x, y, enter, player_idx):
        """Event-Handler für Hover über Zellen."""
        # Handle placement phase hover
        if self.game_phase.state == GameState.Placement and self._is_hover_valid(player_idx):
            if not enter:
                self._clear_hover_highlights(player_idx)
                return
            self._calculate_and_show_hover_highlights(x, y, player_idx)
            return
        
        # Handle extended shooting phase ship hover
        if (self.game_phase.state == GameState.Shooting and 
            isinstance(self.game_phase, ExtendedShootingPhase) and
            player_idx == self.game_phase.current_player_idx):
            self._handle_ship_hover(x, y, enter, player_idx)

    def _is_hover_valid(self, player_idx):
        """Prüft ob Hover für den gegebenen Spieler valid ist."""
        return (self.game_phase.state == GameState.Placement and
                player_idx == self.game_phase.current_player_idx)

    def _clear_hover_highlights(self, player_idx):
        """Löscht alle Hover-Highlights."""
        self.hover_cells = set()
        self.hover_invalid_cells = set()
        self.board_views[player_idx].update()

    def _calculate_and_show_hover_highlights(self, x, y, player_idx):
        """Berechnet und zeigt Hover-Highlights für Objektplatzierung."""
        obj = self.game_phase.current_object
        obj.set_position(x, y)

        board = self.game_phase.players[player_idx].board
        highlight = set(obj.coordinates)

        if self._is_placement_valid(obj, board):
            self.hover_cells = highlight
            self.hover_invalid_cells = set()
        else:
            self.hover_cells = set()
            self.hover_invalid_cells = self._get_invalid_cells(obj, board, highlight)

        self.board_views[player_idx].update(
            highlight_cells=self.hover_cells,
            highlight_invalid_cells=self.hover_invalid_cells
        )

    def _is_placement_valid(self, obj, board):
        """Prüft ob die Objektplatzierung gültig ist."""
        return board.can_place_object(obj)

    def _get_invalid_cells(self, obj, board, highlight):
        """Ermittelt ungültige Zellen für die Objektplatzierung."""
        invalid_cells = set()
        for cx, cy in obj.coordinates:
            if not (0 <= cx < board.width and 0 <= cy < board.height):
                invalid_cells.add((cx, cy))

        # Wenn das Objekt nicht platziert werden kann, alle Zellen als ungültig markieren
        if not board.can_place_object(obj) and not invalid_cells:
            invalid_cells = highlight

        return invalid_cells

    def _handle_ship_hover(self, x, y, enter, player_idx):
        """Handle ship hover in extended shooting phase."""
        if not enter:
            # Clear ship hover when leaving cell
            self.ship_hover_cells = set()
            # Preserve ship selection highlighting when clearing hover
            self.board_views[player_idx].update(
                ship_hover_cells=self.ship_hover_cells,
                ship_selected_cells=self.ship_selected_cells
            )
            return
        
        # Check if there's a ship at this position
        cell = self.game_phase.current_player.board.get_cell(x, y)
        if cell.object and cell.object.coordinates is not None:
            # Highlight all cells of the ship
            self.ship_hover_cells = set(cell.object.coordinates)
        else:
            self.ship_hover_cells = set()
        
        # Update with both hover and selection highlighting
        self.board_views[player_idx].update(
            ship_hover_cells=self.ship_hover_cells,
            ship_selected_cells=self.ship_selected_cells
        )

    def _update_ship_selection_highlighting(self):
        """Update ship selection highlighting for extended shooting phase."""
        if not isinstance(self.game_phase, ExtendedShootingPhase):
            return
        
        # Update selected ship highlighting - verwende active_ship statt selected_ship
        active_ship = (self.game_phase.active_ship if self.game_phase.active_ship 
                       else self.game_phase.selected_ship)
        
        if active_ship:
            self.ship_selected_cells = set(active_ship.coordinates)
        else:
            self.ship_selected_cells = set()
        
        # Update the current player's board with selection highlighting
        current_player_idx = self.game_phase.current_player_idx
        self.board_views[current_player_idx].update(
            ship_hover_cells=self.ship_hover_cells,
            ship_selected_cells=self.ship_selected_cells
        )

    def update_ui(self):
        """
        Zentrale Methode zur Aktualisierung der gesamten UI basierend auf dem aktuellen GameState.

        Diese Methode vereinheitlicht alle UI-Updates und stellt sicher, dass die Benutzeroberfläche
        konsistent mit dem aktuellen Spielzustand ist.
        """
        if not self.game_phase:
            self._update_ui_pregame()
            return

        match self.game_phase.state:
            case GameState.Placement:
                self._update_ui_placement()
            case GameState.Shooting:
                self._update_ui_shooting()
            case GameState.End:
                self._update_ui_end()
            case _:
                self._update_ui_pregame()

    def _update_ui_placement(self):
        """UI-Updates für die Platzierungsphase."""
        # Board-Updates
        self._update_boards_placement()
        
        # Label-Updates
        self.update_current_ship_label()
        
        # Button-Updates
        self._toggle_orientation_button(True)
        self._toggle_auto_place_button(True)
        
        # Hover-State
        for board_view in self.board_views:
            board_view.set_hover_enabled(True)

    def _update_ui_shooting(self):
        """UI-Updates für die Schussphase."""
        # Board-Updates
        self._update_boards_shooting()
        
        # Label-Updates (aktueller Spieler)
        if self.game_phase.current_player is not None:
            self.current_ship_label.config(text=f"{self.game_phase.current_player.name} ist am Zug")
        
        # Button-Updates - unterschiedlich für Extended und Normal Mode
        if isinstance(self.game_phase, ExtendedShootingPhase):
            self._show_button("confirmation")
            # Update selected ship highlighting
            self._update_ship_selection_highlighting()
        else:
            self._show_button("none")
        
        # Hide auto-placement button
        if self.auto_place_button is not None:
            self.auto_place_button.grid_remove()
            self.auto_place_button = None
        
        # Hover-State
        for board_view in self.board_views:
            board_view.set_hover_enabled(True)

    def _update_ui_end(self):
        """UI-Updates für das Spielende."""
        # Alle Boards deaktivieren
        for board_view in self.board_views:
            board_view.set_enabled(False)
            board_view.set_hover_enabled(False)
            board_view.update()
        
        # Label-Updates
        self.current_ship_label.config(text="Spiel beendet")
        
        # Button-Updates
        self._toggle_orientation_button(False)
        if self.auto_place_button is not None:
            self.auto_place_button.grid_remove()
            self.auto_place_button = None

    def _update_ui_pregame(self):
        """UI-Updates für den Pre-Game Zustand."""
        for board_view in self.board_views:
            board_view.set_hover_enabled(False)
            board_view.update()
            board_view.set_enabled(False)
        
        self.current_ship_label.config(text="")
        if self.orientation_button is not None:
            self._toggle_orientation_button(False)
        if self.auto_place_button is not None:
            self.auto_place_button.grid_remove()
            self.auto_place_button = None

    def update_boards(self):
        """Aktualisiert alle Board-Ansichten basierend auf dem aktuellen Spielzustand."""

        # Wenn aktueller Spieler ein Computer ist → kurze Pause einfügen
        if isinstance(self.game_phase.current_player, ComputerPlayer):
            # 500 Millisekunden warten, dann weitermachen
            # time.sleep(self.COMPUTER_TURN_DELAY)
            self._update_boards_internal()
        else:
            self._update_boards_internal()

    def _update_boards_internal(self):
        if self.game_phase.state == GameState.Placement:
            self._update_boards_placement()
        elif self.game_phase.state == GameState.Shooting:
            self._update_boards_shooting()
        else:
            self._update_boards_pregame()

    def _update_boards_placement(self):
        """Aktualisiert Boards für Platzierungsphase."""
        for idx, board_view in enumerate(self.board_views):
            board_view.set_hover_enabled(True)
            is_current_player = idx == self.game_phase.current_player_idx
            is_human = isinstance(self.game_phase.players[idx], HumanPlayer)

            if is_current_player:
                board_view.update(
                    highlight_cells=self.hover_cells,
                    highlight_invalid_cells=self.hover_invalid_cells
                )
                board_view.set_enabled(is_human)
            else:
                board_view.update()
                board_view.set_enabled(False)

    def _update_boards_shooting(self):
        """Aktualisiert Boards für Schussphase."""
        is_human = isinstance(self.game_phase.current_player, HumanPlayer)

        for idx, board_view in enumerate(self.board_views):
            board_view.set_hover_enabled(True)
            board_view.update()

            # Nur gegnerisches Board aktivieren und nur für Menschen
            is_enemy_board = idx == 1 - self.game_phase.current_player_idx
            board_view.set_enabled(is_enemy_board and is_human or isinstance(self.game_phase, ExtendedShootingPhase))

    def _update_boards_pregame(self):
        """Aktualisiert Boards für Pre-Game Zustand."""
        for board_view in self.board_views:
            board_view.set_hover_enabled(False)
            board_view.update()
            board_view.set_enabled(False)

    def run(self):
        self.window.mainloop()
