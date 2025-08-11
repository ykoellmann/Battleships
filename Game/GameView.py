import copy
import tkinter as tk
from tkinter import ttk, messagebox
from typing import List

from Board.Board import Board
from Game.Game import Game
from Game.GameExtended import GameExtended
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
        placement_object_idx (int): Index des aktuell zu platzierenden Objekts.
        hover_cells (set[tuple[int,int]]): Aktuelle Hover-Markierungen gültiger Zellen.
        hover_invalid_cells (set[tuple[int,int]]): Aktuelle Hover-Markierungen ungültiger Zellen.
    """
    COMPUTER_TURN_DELAY = 1000  # Millisekunden
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Schiffe Versenken")
        self.game = None
        self.boards_frame = None

        self.settings_view = SettingsView(self.window, GameSettings(), self.start_game)
        self.settings_view.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

        # Anzeige aktuelles Schiff
        self.current_ship_label = ttk.Label(self.window, text="")
        self.current_ship_label.grid(row=2, column=0, columnspan=2, pady=5)

        # Spielfelder
        self.board_views = []
        self.create_game_boards()

        # Platzierungsstatus
        self.placement_object_idx = 0

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
        if getattr(settings, "mode", "Normal") == "Erweitert":
            game_class = GameExtended
        else:
            game_class = Game

        player1_board = Board()
        player2_board = Board()

        player1 = PlayerFactory.create(settings.p1_type, settings.p1_name, settings.p1_difficulty, player1_board, player2_board)
        player2 = PlayerFactory.create(settings.p2_type, settings.p2_name, settings.p2_difficulty, player2_board, player1_board)

        self.game = game_class(player1, player2, settings=settings)

        self.placement_object_idx = 0
        self.game.current_state = GameState.Placement

        # Setze Boards in BoardViews
        for idx, board_view in enumerate(self.board_views):
            board_view.board = self.game.players[idx].board
            board_view.update()
            board_view.set_hover_enabled(True)

        self._ensure_orientation_button()

        self.update_current_ship_label()
        # Vereinheitlichte Aktivierungslogik: nutze update_boards statt das erste Board standardmäßig zu aktivieren
        self.update_boards()
        # Falls der Startspieler ein Computer ist, platziere automatisch ohne UI-Aktivierung
        self._advance_placement_if_computer()

    def enable_placement_ui(self):
        # Nur das Board des aktuellen Spielers ist aktiv (eigenes Feld)
        for idx, board_view in enumerate(self.board_views):
            if idx == self.game.current_player_idx:
                board_view.set_enabled(True)
            else:
                board_view.set_enabled(False)

        self._ensure_orientation_button()

    def _ensure_orientation_button(self):
        """Stellt sicher, dass der Orientierungsbutton existiert und aktiviert ihn."""
        if not hasattr(self, "orientation_button"):
            self.orientation_button = ttk.Button(
                self.window,
                text="Ausrichtung wechseln",
                command=self.toggle_orientation
            )
            self.orientation_button.grid(row=3, column=0, columnspan=2, pady=5)
        self.orientation_button.state(['!disabled'])

    def toggle_orientation(self):
        """Dreht die Ausrichtung des aktuell zu platzierenden Objekts."""
        obj = self.game.settings.game_objects[self.placement_object_idx]
        obj.rotate()
        self.update_current_ship_label()

    def update_current_ship_label(self):
        if self.game.current_state != GameState.Placement:
            self.current_ship_label.config(text="")
            return

        obj = self.game.settings.game_objects[self.placement_object_idx]
        size = len(obj.coordinates)
        orient = str(obj.orientation)
        self.current_ship_label.config(text=f"{self.game.current_player.name}: Platziere {obj.name} ({size}) [{orient}]")

    def _place_current_for_human(self, x: int, y: int) -> bool:
        """
        Versucht, das aktuelle Objekt des menschlichen Spielers an (x, y) zu platzieren.
        Rückgabe: True bei erfolgreicher Platzierung, sonst False (inkl. Warnung bei ungültiger Position).
        """
        player = self.game.players[self.game.current_player_idx]
        obj = self.game.settings.game_objects[self.placement_object_idx]
        obj_copy = copy.deepcopy(obj)
        obj_copy.set_position(x, y)
        board = player.board
        if not board.can_place_object(obj_copy):
            messagebox.showwarning("Ungültige Platzierung", "Hier kann das Schiff nicht platziert werden!")
            return False
        player.place_object(obj_copy)
        self.placement_object_idx += 1
        self.update_boards()
        return True

    def _finalize_placement_progress(self) -> bool:
        """
        Prüft, ob der aktuelle Spieler alle Objekte platziert hat und führt ggf. den Spielerwechsel
        oder den Übergang in die Schussphase durch. Gibt True zurück, wenn das Spiel gestartet wurde.
        """
        total = len(self.game.settings.game_objects)
        if self.placement_object_idx < total:
            # Noch nicht fertig – nur UI aktualisieren
            self.update_current_ship_label()
            self.update_boards()
            return False

        # Spieler fertig
        self.placement_object_idx = 0
        self.game.current_player_idx += 1
        if self.game.current_player_idx > 1:
            # Beide Spieler fertig → Spielstart
            self.game.current_state = GameState.Shooting
            self.current_ship_label.config(text="")
            if hasattr(self, "orientation_button"):
                self.orientation_button.state(['disabled'])
            self.start_real_game()
            return True

        # Nächster Spieler
        self.update_current_ship_label()
        self.update_boards()
        # Falls nächster Spieler ein Computer ist, automatisch voranschreiten
        self._advance_placement_if_computer()
        return False

    def _advance_placement_if_computer(self):
        """
        Falls der aktuelle Spieler ein Computer ist, platziert er automatisch alle Objekte.
        Wiederhole so lange, bis ein menschlicher Spieler an der Reihe ist oder die Platzierung beendet ist.
        """
        if self.game is None or self.game.current_state != GameState.Placement:
            return
        while (
            self.game.current_state == GameState.Placement and
            not isinstance(self.game.players[self.game.current_player_idx], HumanPlayer)
        ):
            # Computer platziert alle verbleibenden Objekte automatisch
            while self.placement_object_idx < len(self.game.settings.game_objects):
                obj = self.game.settings.game_objects[self.placement_object_idx]
                copy_obj = copy.deepcopy(obj)
                self.game.players[self.game.current_player_idx].place_object(copy_obj)
                self.placement_object_idx += 1
                self.update_boards()
            # Spieler fertig – vereinheitlichter Abschluss & Übergang
            if self._finalize_placement_progress():
                return

    def on_cell_click(self, x, y, player_idx):
        """Event-Handler für Klicks auf Zellen.

        Args:
            x (int): Spaltenindex der Zelle.
            y (int): Zeilenindex der Zelle.
            player_idx (int): Index des Boards (Spielers), auf dem geklickt wurde.
        """
        if self.game.current_state == GameState.Placement:
            if player_idx != self.game.current_player_idx:
                return
            # Nur menschliche Eingabe zulassen (Computer wird automatisch platziert)
            if not isinstance(self.game.players[player_idx], HumanPlayer):
                return
            if not self._place_current_for_human(x, y):
                return
            if self._finalize_placement_progress():
                return
        elif self.game.current_state == GameState.Shooting:
            if self.game.game_over:
                return

            current_idx = self.game.current_player_idx
            if (current_idx == 0 and player_idx != 1) or (current_idx == 1 and player_idx != 0):
                return

            target_board = self.game.players[1 - current_idx].board
            cell = target_board.get_cell(x, y)
            if cell.is_hit or cell.is_miss:
                return

            if self._execute_shot(x, y):
                return

            # Prüfe, ob der nächste Spieler ein Computer ist und lasse ihn schießen
            self.handle_computer_turn()

    def _handle_game_end(self):
        """Behandelt das Spielende einheitlich."""
        if not self.game.game_over:
            return False

        winner = self.game.current_player.name
        messagebox.showinfo("Spielende", f"{winner} hat gewonnen!")
        self.current_ship_label.config(text="Spiel beendet")
        return True

    def _execute_shot(self, x: int, y: int) -> bool:
        """
        Führt einen Schuss aus und behandelt die Konsequenzen.
        
        Returns:
            bool: True wenn das Spiel beendet wurde, False sonst.
        """
        current_idx = self.game.current_player_idx
        target_board = self.game.players[1 - current_idx].board
        
        hit, is_destroyed, game_object = target_board.shoot_at(x, y)
        self.board_views[current_idx].cells_ui[x][y].set_enabled(False)
        
        # Spezielle Behandlung für HardComputerPlayer
        if isinstance(self.game.current_player, HardComputerPlayer):
            self.game.current_player.process_shot_result(
                x, y, hit, is_destroyed, 
                game_object.coordinates if game_object else []
            )
        
        self.update_boards()
        
        if self._handle_game_end():
            return True
        
        # Spielerwechsel nur bei Fehlschuss
        if not hit:
            self._switch_player(hit)
        
        return False

    def _switch_player(self, hit: bool):
        """Wechselt zum nächsten Spieler und aktualisiert UI."""
        if hit:
            return

        self.game.current_player_idx = 1 - self.game.current_player_idx
        self.current_ship_label.config(text=f"{self.game.current_player.name} ist am Zug")
        self.update_boards()

    def start_real_game(self):
        self.game.current_player_idx = 0
        self.game.current_state = GameState.Shooting
        self.update_boards()
        messagebox.showinfo("Spielstart", "Alle Schiffe platziert! Das Spiel beginnt.")
        # Wenn der erste Spieler ein Computer ist, lass ihn sofort schießen
        self.handle_computer_turn()

    def handle_computer_turn(self):
        """Lässt den Computerspieler automatisch schießen, wenn er an der Reihe ist."""

        # Überprüfe, ob das Spiel beendet ist
        if self.game.game_over or self.game.current_state != GameState.Shooting:
            return

        # Überprüfe, ob der aktuelle Spieler ein Computer ist
        current_player = self.game.current_player
        if not isinstance(current_player, ComputerPlayer):
            return

        # Lasse den Computer ein Ziel auswählen
        target = current_player.select_target()
        if target is None:
            return

        x, y = target

        # Führe den Schuss aus
        if self._execute_shot(x, y):
            return

        # Falls der nächste Spieler auch ein Computer ist, rekursiv fortsetzen
        self.window.after(self.COMPUTER_TURN_DELAY, self.handle_computer_turn)

    def create_player(self, player_type, player_name, level, board, opponent_board):
        """Erzeugt einen Spieler anhand der UI-Einstellungen.

        Args:
            player_type (str): "Mensch" oder "Computer".
            player_name (str): Name für menschliche Spieler.
            level (str): Schwierigkeitsgrad für Computer ("leicht"/"schwer"/"unmöglich").
            board (Board): Zugewiesenes Board.
        Returns:
            Player: Instanz von HumanPlayer, EasyComputerPlayer oder HardComputerPlayer.
        """
        if player_type == "Mensch":
            return HumanPlayer(player_name, board)
        elif level.lower() == "leicht":
            return EasyComputerPlayer(board)
        elif level.lower() == "schwer":
            return HardComputerPlayer(board)
        else:
            return ImpossibleComputerPlayer(board, opponent_board)

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
        return (self.game.current_state == GameState.Placement and 
                player_idx == self.game.current_player_idx)

    def _clear_hover_highlights(self, player_idx):
        """Löscht alle Hover-Highlights."""
        self.hover_cells = set()
        self.hover_invalid_cells = set()
        self.board_views[player_idx].update()

    def _calculate_and_show_hover_highlights(self, x, y, player_idx):
        """Berechnet und zeigt Hover-Highlights für Objektplatzierung."""
        obj = self.game.settings.game_objects[self.placement_object_idx]
        obj.set_position(x, y)
        
        board = self.game.players[player_idx].board
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
        if self.game.current_state == GameState.Placement:
            self._update_boards_placement()
        elif self.game.current_state == GameState.Shooting:
            self._update_boards_shooting()
        else:
            self._update_boards_pregame()

    def _update_boards_placement(self):
        """Aktualisiert Boards für Platzierungsphase."""
        for idx, board_view in enumerate(self.board_views):
            board_view.set_hover_enabled(True)
            is_current_player = idx == self.game.current_player_idx
            is_human = isinstance(self.game.players[idx], HumanPlayer)

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
        is_human = isinstance(self.game.current_player, HumanPlayer)

        for idx, board_view in enumerate(self.board_views):
            board_view.set_hover_enabled(True)
            board_view.update()

            # Nur gegnerisches Board aktivieren und nur für Menschen
            is_enemy_board = idx == 1 - self.game.current_player_idx
            board_view.set_enabled(is_enemy_board and is_human)

    def _update_boards_pregame(self):
        """Aktualisiert Boards für Pre-Game Zustand."""
        for board_view in self.board_views:
            board_view.set_hover_enabled(False)
            board_view.update()
            board_view.set_enabled(False)

    def _update_ui_for_game_state(self):
        """Aktualisiert die gesamte UI basierend auf dem aktuellen Spielzustand."""
        if self.game.current_state == GameState.Placement:
            self._ensure_orientation_button()
            self.update_current_ship_label()
        elif self.game.current_state == GameState.Shooting:
            self._disable_orientation_button()
            self._update_current_player_label()
        
        self.update_boards()

    def _disable_orientation_button(self):
        """Deaktiviert den Orientierungsbutton."""
        if hasattr(self, "orientation_button"):
            self.orientation_button.state(['disabled'])

    def _update_current_player_label(self):
        """Aktualisiert das Label für den aktuellen Spieler."""
        if self.game.current_state == GameState.Shooting:
            self.current_ship_label.config(text=f"{self.game.current_player.name} ist am Zug")

    def run(self):
        self.window.mainloop()
