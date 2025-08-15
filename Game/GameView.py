import copy
import tkinter as tk
import time
from tkinter import ttk, messagebox
from typing import List

from Board.Board import Board
from Game.GamePhase.PlacementPhase import PlacementPhase
from Game.GamePhase.ShootingPhase import ShootingPhase
from Objects.GameObject import GameObject
from Player.Computer.ComputerPlayer import ComputerPlayer
from Player.Computer.ImpossibleComputerPlayer import ImpossibleComputerPlayer
from Player.Player import Player
from Player.PlayerFactory import PlayerFactory
from Utils.Orientation import Orientation
from Player.Computer.EasyComputerPlayer import EasyComputerPlayer
from Player.HumanPlayer import HumanPlayer
from Player.Computer.HardComputerPlayer import HardComputerPlayer

from Game.BoardView import BoardView
from Game.SettingsView import SettingsView, GameSettings
from Utils.GameState import GameState


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
        self.game_phase = None
        self.boards_frame = None

        self.settings_view = SettingsView(self.window, GameSettings(), self.start_game)
        self.settings_view.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

        # Anzeige aktuelles Schiff
        self.current_ship_label = ttk.Label(self.window, text="")
        self.current_ship_label.grid(row=2, column=0, columnspan=2, pady=5)

        # Spielfelder
        self.board_views = []
        self.create_game_boards()


        self.hover_cells = set()

    def create_game_boards(self):
        boards_frame = ttk.Frame(self.window, padding=10)
        boards_frame.grid(row=1, column=0, columnspan=2)

        self.boards_frame = boards_frame
        self.board_views.clear()
        for idx in range(2):
            frame = ttk.LabelFrame(boards_frame, text=f"Spieler {idx+1}", padding=5)
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
        settings = self.settings_view.settings
        if settings.mode == "Erweitert":
            game_phase_class = PlacementPhase
        else:
            game_phase_class = PlacementPhase

        player1_board = Board()
        player2_board = Board()

        player1 = PlayerFactory.create(settings.p1_type, settings.p1_name, settings.p1_difficulty, player1_board, player2_board)
        player2 = PlayerFactory.create(settings.p2_type, settings.p2_name, settings.p2_difficulty, player2_board, player1_board)

        self.game_phase = game_phase_class(player1, player2, self.placement_callback, settings=settings)

        # Setze Boards in BoardViews
        for idx, board_view in enumerate(self.board_views):
            board_view.board = self.game_phase.players[idx].board
            board_view.update()
            board_view.set_hover_enabled(True)

        self._toggle_orientation_button(True)

        self.update_current_ship_label()
        # Vereinheitlichte Aktivierungslogik: nutze update_boards statt das erste Board standardmäßig zu aktivieren
        self.update_boards()
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
        if not hasattr(self, "orientation_button"):
            self.orientation_button = ttk.Button(
                self.window,
                text="Ausrichtung wechseln",
                command=self.game_phase.toggle_orientation,
            )
            self.orientation_button.grid(row=3, column=0, columnspan=2, pady=5)

        state = "disabled"
        if enabled:
            state = "!" + state
        self.orientation_button.state([state])


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
        self.game_phase.handle_cell_click(x, y)
        # if self.game_phase.state == GameState.Placement:
        #     is_placed, is_over = self.game_phase.handle_cell_click(x, y)
        #
        #     if not is_placed:
        #         messagebox.showwarning("Ungültige Platzierung", "Hier kann das Schiff nicht platziert werden!")
        #         return
        #
        #     if is_over:
        #         self.game_phase = ShootingPhase(self.game_phase.players[0], self.game_phase.players[1], self.shooting_callback)
        #         self.game_phase.window = self.window
        #         self.current_ship_label.config(text="")
        #         if hasattr(self, "orientation_button"):
        #             self.orientation_button.state(['disabled'])
        #         self.start_real_game()
        #
        #     self.update_current_ship_label()
        #     self.update_boards()
        # elif self.game_phase.state == GameState.Shooting:
        #     self.game_phase.handle_cell_click(x, y)

    def shooting_callback(self, hit, is_over):
        if not hit:
            self.current_ship_label.config(text=f"{self.game_phase.current_player.name} ist am Zug")

        if is_over:
            self._handle_game_end()
        self.update_boards()

    def placement_callback(self, is_placed, is_over):
        if not is_placed:
            messagebox.showwarning("Ungültige Platzierung", "Hier kann das Schiff nicht platziert werden!")
            return

        if is_over:
            self.game_phase = ShootingPhase(self.game_phase.players[0], self.game_phase.players[1],
                                            self.shooting_callback)
            self.game_phase.window = self.window
            self.current_ship_label.config(text="")
            if hasattr(self, "orientation_button"):
                self.orientation_button.state(['disabled'])
            self.start_real_game()

        self.update_current_ship_label()
        self.update_boards()


    def _handle_game_end(self):
        """Behandelt das Spielende einheitlich."""
        if not self.game_phase.is_over():
            return False

        winner = self.game_phase.current_player.name
        messagebox.showinfo("Spielende", f"{winner} hat gewonnen!")
        self.current_ship_label.config(text="Spiel beendet")
        return True

    # def _execute_shot(self, x: int, y: int) -> bool:
    #     """
    #     Führt einen Schuss aus und behandelt die Konsequenzen.
    #
    #     Returns:
    #         bool: True wenn das Spiel beendet wurde, False sonst.
    #     """
    #     current_idx = self.game.current_player_idx
    #     target_board = self.game.players[1 - current_idx].board
    #
    #     hit, is_destroyed, game_object = target_board.shoot_at(x, y)
    #     self.board_views[current_idx].cells_ui[x][y].set_enabled(False)
    #
    #     # Spezielle Behandlung für HardComputerPlayer
    #     if isinstance(self.game.current_player, HardComputerPlayer):
    #         self.game.current_player.process_shot_result(
    #             x, y, hit, is_destroyed,
    #             game_object.coordinates if game_object else []
    #         )
    #
    #     self.update_boards()
    #
    #     if self._handle_game_end():
    #         return True
    #
    #     # Spielerwechsel nur bei Fehlschuss
    #     if not hit:
    #         self._switch_player(hit)
    #
    #     return False

    def start_real_game(self):
        self.update_boards()
        messagebox.showinfo("Spielstart", "Alle Schiffe platziert! Das Spiel beginnt.")
        # Wenn der erste Spieler ein Computer ist, lass ihn sofort schießen
        self.game_phase.next_turn(False)

    def on_cell_hover(self, x, y, enter, player_idx):
        """Event-Handler für Hover über Zellen in der Platzierungsphase."""
        if not self._is_hover_valid(player_idx):
            return

        if not enter:
            self._clear_hover_highlights(player_idx)
            return

        self._calculate_and_show_hover_highlights(x, y, player_idx)

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
                    highlight_cells=getattr(self, "hover_cells", set()),
                    highlight_invalid_cells=getattr(self, "hover_invalid_cells", set())
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
            board_view.set_enabled(is_enemy_board and is_human)

    def _update_boards_pregame(self):
        """Aktualisiert Boards für Pre-Game Zustand."""
        for board_view in self.board_views:
            board_view.set_hover_enabled(False)
            board_view.update()
            board_view.set_enabled(False)

    # def _update_ui_for_game_state(self):
    #     """Aktualisiert die gesamte UI basierend auf dem aktuellen Spielzustand."""
    #     if self.game.current_state == GameState.Placement:
    #         self._toggle_orientation_button(True)
    #         self.update_current_ship_label()
    #     elif self.game.current_state == GameState.Shooting:
    #         self._toggle_orientation_button(False)
    #         self._update_current_player_label()
    #
    #     self.update_boards()

    # def _update_current_player_label(self):
    #     """Aktualisiert das Label für den aktuellen Spieler."""
    #     if self.game.current_state == GameState.Shooting:
    #         self.current_ship_label.config(text=f"{self.game.current_player.name} ist am Zug")

    def run(self):
        self.window.mainloop()
