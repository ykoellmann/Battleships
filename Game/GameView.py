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
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Schiffe Versenken")
        self.game = None

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
            dummy_board = Board()
            board_view = BoardView(
                frame,
                dummy_board,
                cell_size=32,
                click_callback=lambda x, y, p=idx: self.on_cell_click(x, y, p),
                hover_callback=lambda x, y, enter, p=idx: self.on_cell_hover(x, y, enter, p)
            )
            board_view.pack()
            # Hover im Pre-Game deaktiviert
            board_view.set_hover_enabled(False)
            self.board_views.append(board_view)

    def start_game(self):
        settings = self.settings_view.settings
        if getattr(settings, "mode", "Normal") == "Erweitert":
            game_class = GameExtended
        else:
            game_class = Game

        player1_board = Board()
        player2_board = Board()

        players = [
            self.create_player(settings.p1_type, settings.p1_name, settings.p1_difficulty, player1_board, player2_board),
            self.create_player(settings.p2_type, settings.p2_name, settings.p2_difficulty, player2_board, player1_board)
        ]
        self.game = game_class(players[0], players[1], settings=settings)

        self.placement_object_idx = 0

        self.game.current_player_idx = 0
        self.game.current_state = GameState.Placement

        # Setze Boards in BoardViews
        for idx, board_view in enumerate(self.board_views):
            board_view.board = self.game.players[idx].board
            board_view.update()
            board_view.set_hover_enabled(True)

        # Erstelle/aktiviere Orientierungs-Button falls nötig
        if not hasattr(self, "orientation_button"):
            self.orientation_button = ttk.Button(self.window, text="Ausrichtung wechseln",
                                                 command=self.toggle_orientation)
            self.orientation_button.grid(row=3, column=0, columnspan=2, pady=5)
        self.orientation_button.state(['!disabled'])

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

        # Taste für Orientierung
        if not hasattr(self, "orientation_button"):
            self.orientation_button = ttk.Button(self.window, text="Ausrichtung wechseln",
                                                 command=self.toggle_orientation)
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
        player = "Spieler 1" if self.game.current_player_idx == 0 else "Spieler 2"
        obj = self.game.settings.game_objects[self.placement_object_idx]
        name = type(obj).__name__
        size = len(obj.coordinates)
        orient = "Horizontal" if obj.orientation == Orientation.HORIZONTAL else "Vertikal"
        self.current_ship_label.config(text=f"{player}: Platziere {name} ({size}) [{orient}]")

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

            target_board.shoot_at(x, y)
            self.board_views[current_idx].cells_ui[x][y].set_enabled(False)
            self.update_boards()

            if self.game.game_over:
                winner = self.game.current_player.name
                messagebox.showinfo("Spielende", f"{winner} hat gewonnen!")
                self.current_ship_label.config(text="Spiel beendet")
                return

            # Wechsle Spieler nach jedem Schuss
            self.game.current_player_idx = 1 - self.game.current_player_idx
            self.current_ship_label.config(text=f"{self.game.current_player.name} ist am Zug")
            self.update_boards()

            # Prüfe, ob der nächste Spieler ein Computer ist und lasse ihn schießen
            self.handle_computer_turn()

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
        current_idx = self.game.current_player_idx
        if not isinstance(current_player, ComputerPlayer):
            return

        # Lasse den Computer ein Ziel auswählen
        target = current_player.select_target()
        if target is None:
            return

        x, y = target

        # Führe den Schuss aus
        target_board = self.game.other_player.board
        hit, is_destroyed, game_object = target_board.shoot_at(x, y)
        self.board_views[current_idx].cells_ui[x][y].set_enabled(False)

        if isinstance(current_player, HardComputerPlayer):
            current_player.process_shot_result(x, y, hit, is_destroyed, game_object.coordinates if game_object else [])

        self.update_boards()

        # Überprüfe, ob das Spiel beendet ist
        if self.game.game_over:
            winner = self.game.current_player.name
            messagebox.showinfo("Spielende", f"{winner} hat gewonnen!")
            self.current_ship_label.config(text="Spiel beendet")
            return

        # Wechsle zum anderen Spieler
        self.game.current_player_idx = 1 - self.game.current_player_idx
        self.current_ship_label.config(text=f"{self.game.current_player.name} ist am Zug")
        self.update_boards()

        # Falls der nächste Spieler auch ein Computer ist, rekursiv fortsetzen
        self.window.after(1000, self.handle_computer_turn)

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
        """Event-Handler für Hover über Zellen in der Platzierungsphase.

        Args:
            x (int): Spaltenindex der Zelle.
            y (int): Zeilenindex der Zelle.
            enter (bool): True bei Enter, False bei Leave.
            player_idx (int): Index des betroffenen Boards (Spielers).
        """
        if self.game.current_state != GameState.Placement:
            return
        if player_idx != self.game.current_player_idx:
            return
        if not enter:
            self.hover_cells = set()
            self.hover_invalid_cells = set()
            self.board_views[player_idx].update()
            return
        # Hole aktuelles Schiff und berechne belegte Zellen
        obj = self.game.settings.game_objects[self.placement_object_idx]
        obj.set_position(x, y)
        highlight = set(obj.coordinates)
        board = self.game.players[player_idx].board

        # Prüfe, ob alle Zellen im Board sind und frei (keine Überschneidung)
        valid = True
        invalid_cells = set()
        for cx, cy in obj.coordinates:
            if not (0 <= cx < board.width and 0 <= cy < board.height):
                valid = False
                invalid_cells.add((cx, cy))
            elif not board.can_place_object(obj):
                # Wenn das Schiff insgesamt nicht platziert werden kann, alle Zellen als ungültig markieren
                invalid_cells = highlight
                valid = False
                break
        if valid:
            self.hover_cells = highlight
            self.hover_invalid_cells = set()
        else:
            self.hover_cells = set()
            self.hover_invalid_cells = invalid_cells
        self.board_views[player_idx].update(
            highlight_cells=self.hover_cells,
            highlight_invalid_cells=self.hover_invalid_cells
        )

    def update_boards(self):
        for idx, board_view in enumerate(self.board_views):
            board = self.game.players[idx].board
            # Platzierungsphase: Nur das eigene Feld ist aktiv
            if self.game.current_state == GameState.Placement:
                board_view.set_hover_enabled(True)
                if idx == self.game.current_player_idx:
                    board_view.update(
                        highlight_cells=getattr(self, "hover_cells", set()),
                        highlight_invalid_cells=getattr(self, "hover_invalid_cells", set())
                    )
                    # Aktiviere nur, wenn aktueller Spieler ein Mensch ist
                    if isinstance(self.game.players[idx], HumanPlayer):
                        board_view.set_enabled(True)
                    else:
                        board_view.set_enabled(False)
                else:
                    board_view.update()
                    board_view.set_enabled(False)
            # Schussphase: Nur das gegnerische Feld ist aktiv
            elif self.game.current_state == GameState.Shooting:
                board_view.set_hover_enabled(True)
                # Nur das gegnerische Feld aktivieren und nur für menschliche Spieler
                is_human = isinstance(self.game.current_player, HumanPlayer)

                if idx == 1 - self.game.current_player_idx and is_human:
                    board_view.update()
                    board_view.set_enabled(True)
                else:
                    board_view.update()
                    board_view.set_enabled(False)
            else:
                # Pre-Game oder andere Zustände
                board_view.set_hover_enabled(False)
                board_view.update()
                board_view.set_enabled(False)

    def run(self):
        self.window.mainloop()
