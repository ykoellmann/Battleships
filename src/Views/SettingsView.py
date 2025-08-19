import tkinter as tk
from tkinter import ttk

from src.Utils.constants import PlayerType, GameMode, GameConstants, UIColors
from src.Utils.GameSettings import GameSettings


class SettingsView(tk.Frame):
    def __init__(self, master, settings: GameSettings, on_start_game):
        """
        master: Tkinter parent widget
        settings: GameSettings-Objekt für aktuelle Einstellungen
        on_start_game: Callback, wird mit settings aufgerufen wenn "Spiel starten" geklickt wird
        """
        super().__init__(master, padx=10, pady=10, bg=UIColors.FRAME_BG)
        self.settings = settings
        self.on_start_game = on_start_game

        self._build_ui()

    def _build_ui(self):
        tk.Label(self, text="Spiel-Einstellungen", font=("Arial", 14, "bold"), 
                 bg=UIColors.FRAME_BG, fg=UIColors.BUTTON_FG).grid(row=0, column=0, columnspan=3, pady=5)

        # Spieler 1
        tk.Label(self, text="Spieler 1:", bg=UIColors.FRAME_BG, fg=UIColors.BUTTON_FG).grid(row=1, column=0, sticky="w")
        self.p1_type = tk.StringVar(value=self.settings.p1_type)
        self.p1_type_combo = ttk.Combobox(self, textvariable=self.p1_type, values=GameConstants.PLAYER_TYPE_OPTIONS, state="readonly", width=10, style='Brown.TCombobox')
        self.p1_type_combo.grid(row=1, column=1, sticky="ew")
        self.p1_type_combo.bind("<<ComboboxSelected>>", lambda e: self._update_player_fields(1))

        self.p1_name_var = tk.StringVar(value=self.settings.p1_name)
        self.p1_name_entry = tk.Entry(self, textvariable=self.p1_name_var, bg=UIColors.BUTTON_BG, fg=UIColors.BUTTON_FG)

        self.p1_diff_var = tk.StringVar(value=self.settings.p1_difficulty)
        self.p1_diff_combo = ttk.Combobox(self, textvariable=self.p1_diff_var, values=GameConstants.DIFFICULTY_OPTIONS, state="readonly", width=10, style='Brown.TCombobox')

        # Spieler 2
        tk.Label(self, text="Spieler 2:", bg=UIColors.FRAME_BG, fg=UIColors.BUTTON_FG).grid(row=2, column=0, sticky="w")
        self.p2_type = tk.StringVar(value=self.settings.p2_type)
        self.p2_type_combo = ttk.Combobox(self, textvariable=self.p2_type, values=GameConstants.PLAYER_TYPE_OPTIONS, state="readonly", width=10, style='Brown.TCombobox')
        self.p2_type_combo.grid(row=2, column=1, sticky="ew")
        self.p2_type_combo.bind("<<ComboboxSelected>>", lambda e: self._update_player_fields(2))

        self.p2_name_var = tk.StringVar(value=self.settings.p2_name)
        self.p2_name_entry = tk.Entry(self, textvariable=self.p2_name_var, bg=UIColors.BUTTON_BG, fg=UIColors.BUTTON_FG)

        self.p2_diff_var = tk.StringVar(value=self.settings.p2_difficulty)
        self.p2_diff_combo = ttk.Combobox(self, textvariable=self.p2_diff_var, values=GameConstants.DIFFICULTY_OPTIONS, state="readonly", width=10, style='Brown.TCombobox')

        # Spielmodus
        tk.Label(self, text="Spielmodus:", bg=UIColors.FRAME_BG, fg=UIColors.BUTTON_FG).grid(row=3, column=0, sticky="w")
        self.mode_var = tk.StringVar(value=self.settings.mode)
        tk.Radiobutton(self, text="Normal", variable=self.mode_var, value=GameMode.STANDARD.value,
                       bg=UIColors.FRAME_BG, fg=UIColors.BUTTON_FG, selectcolor=UIColors.BUTTON_BG).grid(row=3, column=1, sticky="w")
        tk.Radiobutton(self, text="Erweitert", variable=self.mode_var, value=GameMode.EXTENDED.value,
                       bg=UIColors.FRAME_BG, fg=UIColors.BUTTON_FG, selectcolor=UIColors.BUTTON_BG).grid(row=3, column=2, sticky="w")

        # Button Spiel starten
        start_btn = tk.Button(self, text="Spiel starten", command=self._start_game,
                              bg=UIColors.BUTTON_BG, fg=UIColors.BUTTON_FG, activebackground=UIColors.BUTTON_ACTIVE_BG)
        start_btn.grid(row=4, column=0, columnspan=3, pady=10)

        # Initialfelder setzen
        self._update_player_fields(1)
        self._update_player_fields(2)

        self.columnconfigure(1, weight=1)

    def _update_player_fields(self, player_num):
        """
        Show name field or difficulty field depending on player type.
        
        Args:
            player_num: Player number (1 or 2) to update fields for
        """
        if player_num == 1:
            self.p1_name_entry.grid_forget()
            self.p1_diff_combo.grid_forget()
            if self.p1_type.get() == PlayerType.HUMAN.value:
                self.p1_name_entry.grid(row=1, column=2, sticky="ew")
            else:
                self.p1_diff_combo.grid(row=1, column=2, sticky="ew")
        elif player_num == 2:
            self.p2_name_entry.grid_forget()
            self.p2_diff_combo.grid_forget()
            if self.p2_type.get() == PlayerType.HUMAN.value:
                self.p2_name_entry.grid(row=2, column=2, sticky="ew")
            else:
                self.p2_diff_combo.grid(row=2, column=2, sticky="ew")

    def _start_game(self):
        """Speichert die UI-Werte ins Settings-Objekt und ruft Callback auf."""
        self.settings.p1_type = self.p1_type.get()
        self.settings.p2_type = self.p2_type.get()
        self.settings.p1_name = self.p1_name_var.get()
        self.settings.p2_name = self.p2_name_var.get()
        self.settings.p1_difficulty = self.p1_diff_var.get()
        self.settings.p2_difficulty = self.p2_diff_var.get()
        self.settings.mode = self.mode_var.get()

        if self.on_start_game:
            self.on_start_game()
