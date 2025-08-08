import tkinter as tk
from tkinter import ttk, messagebox

from Board.Board import Board
from Game import Game
from Objects.Ships.Battleship import Battleship
from Objects.Ships.Cruiser import Cruiser
from Objects.Ships.Destroyer import Destroyer
from Objects.Ships.Submarine import Submarine
from Objects.Utils.Orientation import Orientation
from Player.Computer.EasyComputerPlayer import EasyComputerPlayer
from Player.HumanPlayer import HumanPlayer
from Player.Computer.HardComputerPlayer import HardComputerPlayer  # Import für schweren Computer


class GameUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Schiffe Versenken")
        self.game = None

        # Variablen für Schwierigkeitsgrad
        self.player1_level_var = tk.StringVar(value="leicht")
        self.player2_level_var = tk.StringVar(value="leicht")
        self.objects = [
            Battleship(Orientation.HORIZONTAL),  # 1x Schlachtschiff (5 Felder)
            Cruiser(Orientation.HORIZONTAL),  # 2x Kreuzer (4 Felder)
            Cruiser(Orientation.HORIZONTAL),
            Destroyer(Orientation.HORIZONTAL),  # 3x Zerstörer (3 Felder)
            Destroyer(Orientation.HORIZONTAL),
            Destroyer(Orientation.HORIZONTAL),
            Submarine(Orientation.HORIZONTAL),  # 4x U-Boot (2 Felder)
            Submarine(Orientation.HORIZONTAL),
            Submarine(Orientation.HORIZONTAL),
            Submarine(Orientation.HORIZONTAL)
        ]

        # Für Platzierungslogik
        self.placement_phase = True
        self.placement_player_idx = 0  # 0 = Spieler 1, 1 = Spieler 2
        self.placement_object_idx = 0
        self.placement_players = []
        self.placement_boards = []
        self.placement_objects = []
        self.placement_orientation = Orientation.HORIZONTAL

        self.setup_ui()

    def setup_ui(self):
        # Einstellungen Frame
        settings_frame = ttk.LabelFrame(self.window, text="Spieleinstellungen", padding=10)
        settings_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

        # Spieler 1 Einstellungen
        ttk.Label(settings_frame, text="Spieler 1:").grid(row=0, column=0, padx=5)
        self.player1_var = tk.StringVar(value="Mensch")
        player1_menu = ttk.OptionMenu(settings_frame, self.player1_var, "Mensch", "Mensch", "Computer",
                                      command=lambda _: self.update_player1_input())
        player1_menu.grid(row=0, column=1, padx=5)

        # Eingabefeld/Dropdown für Spieler 1
        self.player1_name = ttk.Entry(settings_frame, width=15)
        self.player1_name.grid(row=0, column=2, padx=5)
        self.player1_level_menu = ttk.OptionMenu(settings_frame, self.player1_level_var, "leicht", "leicht", "schwer")
        # Wird dynamisch angezeigt/versteckt

        # Spieler 2 Einstellungen
        ttk.Label(settings_frame, text="Spieler 2:").grid(row=0, column=3, padx=5)
        self.player2_var = tk.StringVar(value="")
        player2_menu = ttk.OptionMenu(settings_frame, self.player2_var, "Computer", "Mensch", "Computer",
                                      command=lambda _: self.update_player2_input())
        player2_menu.grid(row=0, column=4, padx=5)

        # Eingabefeld/Dropdown für Spieler 2
        self.player2_name = ttk.Entry(settings_frame, width=15)
        self.player2_name.grid(row=0, column=5, padx=5)
        self.player2_level_menu = ttk.OptionMenu(settings_frame, self.player2_level_var, "leicht", "leicht", "schwer")
        # Wird dynamisch angezeigt/versteckt

        # Start Button
        self.start_button = ttk.Button(settings_frame, text="Spiel starten", command=self.start_game)
        self.start_button.grid(row=0, column=6, padx=20)

        # Anzeige aktuelles Schiff
        self.current_ship_label = ttk.Label(self.window, text="")
        self.current_ship_label.grid(row=2, column=0, columnspan=2, pady=5)

        # Initiale Anzeige der Eingabefelder
        self.update_player1_input()
        self.update_player2_input()

        # Spielfelder
        self.create_game_boards()

    def update_player1_input(self):
        # Zeige je nach Auswahl Entry oder Dropdown
        if self.player1_var.get() == "Computer":
            self.player1_name.grid_remove()
            self.player1_level_menu.grid(row=0, column=2, padx=5)
        else:
            self.player1_level_menu.grid_remove()
            self.player1_name.grid(row=0, column=2, padx=5)

    def update_player2_input(self):
        if self.player2_var.get() == "Computer":
            self.player2_name.grid_remove()
            self.player2_level_menu.grid(row=0, column=5, padx=5)
        else:
            self.player2_level_menu.grid_remove()
            self.player2_name.grid(row=0, column=5, padx=5)

    def create_game_boards(self):
        # Spielfeld Container
        boards_frame = ttk.Frame(self.window, padding=10)
        boards_frame.grid(row=1, column=0, columnspan=2)

        # Spielfeld 1
        board1_frame = ttk.LabelFrame(boards_frame, text="Spieler 1", padding=5)
        board1_frame.grid(row=0, column=0, padx=10)
        self.board1_buttons = self.create_board_grid(board1_frame, player_idx=0)

        # Spielfeld 2
        board2_frame = ttk.LabelFrame(boards_frame, text="Spieler 2", padding=5)
        board2_frame.grid(row=0, column=1, padx=10)
        self.board2_buttons = self.create_board_grid(board2_frame, player_idx=1)

    def create_board_grid(self, parent, player_idx):
        buttons = []
        for i in range(10):
            row = []
            for j in range(10):
                btn = ttk.Button(parent, width=3)
                btn.grid(row=i, column=j, padx=1, pady=1)
                btn.config(command=lambda x=i, y=j, p=player_idx: self.on_cell_click(x, y, p))
                # Mouse-Events für Hover
                btn.bind("<Enter>", lambda e, x=i, y=j, p=player_idx: self.on_cell_hover(x, y, p, True))
                btn.bind("<Leave>", lambda e, x=i, y=j, p=player_idx: self.on_cell_hover(x, y, p, False))
                row.append(btn)
            buttons.append(row)
        return buttons

    def start_game(self):
        # Spieler und Boards vorbereiten
        self.placement_phase = True
        self.placement_player_idx = 0
        self.placement_object_idx = 0
        self.placement_players = [
            self.create_player(self.player1_var.get(), self.player1_name.get(), self.player1_level_var.get(), Board()),
            self.create_player(self.player2_var.get(), self.player2_name.get(), self.player2_level_var.get(), Board())
        ]
        self.placement_boards = [self.placement_players[0].board, self.placement_players[1].board]
        self.placement_objects = [self.objects.copy(), self.objects.copy()]
        self.placement_orientation = Orientation.HORIZONTAL

        self.update_boards()
        self.update_current_ship_label()
        self.enable_placement_ui()

    def enable_placement_ui(self):
        # Buttons für Platzierung aktivieren/deaktivieren
        # Nur das Board des aktuellen Spielers ist aktiv
        for x in range(10):
            for y in range(10):
                if self.placement_player_idx == 0:
                    self.board1_buttons[x][y].state(['!disabled'])
                    self.board2_buttons[x][y].state(['disabled'])
                else:
                    self.board1_buttons[x][y].state(['disabled'])
                    self.board2_buttons[x][y].state(['!disabled'])

        # Taste für Orientierung
        if not hasattr(self, "orientation_button"):
            self.orientation_button = ttk.Button(self.window, text="Ausrichtung wechseln",
                                                 command=self.toggle_orientation)
            self.orientation_button.grid(row=3, column=0, columnspan=2, pady=5)
        self.orientation_button.state(['!disabled'])

    def toggle_orientation(self):
        self.placement_orientation = (
            Orientation.VERTICAL if self.placement_orientation == Orientation.HORIZONTAL else Orientation.HORIZONTAL
        )
        self.update_current_ship_label()

    def update_current_ship_label(self):
        if not self.placement_phase:
            self.current_ship_label.config(text="")
            return
        player = "Spieler 1" if self.placement_player_idx == 0 else "Spieler 2"
        obj = self.placement_objects[self.placement_player_idx][self.placement_object_idx]
        name = type(obj).__name__
        size = len(obj.coordinates)
        orient = "Horizontal" if self.placement_orientation == Orientation.HORIZONTAL else "Vertikal"
        self.current_ship_label.config(text=f"{player}: Platziere {name} ({size}) [{orient}]")

    def on_cell_hover(self, x, y, player_idx, enter):
        # Nur für HumanPlayer und nur im Placement
        if not self.placement_phase or player_idx != self.placement_player_idx:
            return
        player = self.placement_players[player_idx]
        if not isinstance(player, HumanPlayer):
            return
        obj = self.placement_objects[player_idx][self.placement_object_idx]
        obj.orientation = self.placement_orientation
        obj.set_position(x, y)
        board = self.placement_boards[player_idx]
        # Markiere Zellen beim Hovern
        if enter:
            if board.can_place_object(obj):
                for cx, cy in obj.coordinates:
                    self.get_board_buttons(player_idx)[cx][cy].config(style='Ship.TButton')
                # Adjacent markieren
                for cell in board.get_adjacent_cells(obj):
                    if not cell.is_occupied():
                        self.get_board_buttons(player_idx)[cell.x][cell.y].config(style='Miss.TButton')
            else:
                for cx, cy in obj.coordinates:
                    if 0 <= cx < 10 and 0 <= cy < 10:
                        self.get_board_buttons(player_idx)[cx][cy].config(style='Hit.TButton')
        else:
            self.update_boards()

    def on_cell_click(self, x, y, player_idx):
        if self.placement_phase:
            player = self.placement_players[player_idx]
            obj = self.placement_objects[player_idx][self.placement_object_idx]
            obj.orientation = self.placement_orientation
            obj.set_position(x, y)
            board = self.placement_boards[player_idx]
            if isinstance(player, HumanPlayer):
                if not board.can_place_object(obj):
                    messagebox.showwarning("Ungültige Platzierung", "Hier kann das Schiff nicht platziert werden!")
                    return
                player.place_object(obj)
                self.placement_object_idx += 1
            else:
                # Computer platziert alle Schiffe automatisch, einzeln und gültig
                import random
                while self.placement_object_idx < len(self.placement_objects[player_idx]):
                    obj = self.placement_objects[player_idx][self.placement_object_idx]
                    player.place_object(obj)
                    self.placement_object_idx += 1
            if self.placement_object_idx >= len(self.placement_objects[player_idx]):
                # Nächster Spieler oder Spielstart
                self.placement_object_idx = 0
                self.placement_player_idx += 1
                if self.placement_player_idx > 1:
                    self.placement_phase = False
                    self.current_ship_label.config(text="")
                    self.orientation_button.state(['disabled'])
                    self.start_real_game()
                    return
                # Falls nächster Spieler ein Computer ist, platziere automatisch
                if not isinstance(self.placement_players[self.placement_player_idx], HumanPlayer):
                    # Automatische Platzierung für Computer
                    import random
                    while self.placement_object_idx < len(self.placement_objects[self.placement_player_idx]):
                        obj = self.placement_objects[self.placement_player_idx][self.placement_object_idx]
                        self.placement_players[self.placement_player_idx].place_object(obj)
                        self.placement_object_idx += 1
                    self.placement_object_idx = len(self.placement_objects[self.placement_player_idx])
                    self.placement_player_idx += 1
                    if self.placement_player_idx > 1:
                        self.placement_phase = False
                        self.current_ship_label.config(text="")
                        self.orientation_button.state(['disabled'])
                        self.start_real_game()
                        return
        else:
            # Schussphase
            if self.game.game_over:
                return

            current_idx = self.game.current_player_idx
            # Spieler 1 darf nur auf Board 2 schießen, Spieler 2 nur auf Board 1
            if (current_idx == 0 and player_idx != 1) or (current_idx == 1 and player_idx != 0):
                return

            # Prüfe, ob Feld schon beschossen wurde
            target_board = self.placement_boards[1 - current_idx]
            cell = target_board.get_cell(x, y)
            if cell.is_hit() or cell.is_miss():
                return

            hit = self.game.make_turn(x, y)
            self.update_boards()

            if self.game.game_over:
                winner = self.get_current_player_name()
                messagebox.showinfo("Spielende", f"{winner} hat gewonnen!")
                self.current_ship_label.config(text="Spiel beendet")
                self.enable_gameplay_ui()
                return

            # Spielerwechsel falls nötig
            if not hit:
                self.current_ship_label.config(text=f"{self.get_current_player_name()} ist am Zug")

    def get_board_buttons(self, player_idx):
        return self.board1_buttons if player_idx == 0 else self.board2_buttons

    def start_real_game(self):
        # Starte das eigentliche Spiel mit den platzierten Spielern
        self.game = Game(self.placement_players[0], self.placement_players[1])
        self.update_boards()
        messagebox.showinfo("Spielstart", "Alle Schiffe platziert! Das Spiel beginnt.")

    def create_player(self, player_type, player_name, level, board):
        if player_type == "Mensch":
            return HumanPlayer(player_name, board)
        elif level == "leicht":
            return EasyComputerPlayer(board)
        else:
            return HardComputerPlayer(board)

    def update_boards(self):
        # Zeige Schiffe nur beim Platzieren für den aktiven Spieler, sonst nicht
        for idx, buttons in enumerate([self.board1_buttons, self.board2_buttons]):
            board = self.placement_boards[idx] if self.placement_phase else self.game.players[idx].board
            for x in range(10):
                for y in range(10):
                    cell = board.get_cell(x, y)
                    btn = buttons[x][y]
                    self.update_cell_button(btn, cell,
                                            show_ships=(self.placement_phase and idx == self.placement_player_idx))

    def update_cell_button(self, button, cell, show_ships=False):
        if cell.is_hit():
            button.config(style='Hit.TButton')
        elif cell.is_miss():
            button.config(style='Miss.TButton')
        elif cell.is_occupied() and show_ships:
            button.config(style='Ship.TButton')
        else:
            button.config(style='Empty.TButton')

    def run(self):
        # Button-Styles definieren
        style = ttk.Style()
        style.configure('Hit.TButton', background='red')
        style.configure('Miss.TButton', background='blue')
        style.configure('Ship.TButton', background='gray')
        style.configure('Empty.TButton', background='white')

        self.window.mainloop()
