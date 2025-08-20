import tkinter as tk

from src.Core.Board.Cell import Cell, CellState
from src.Utils.Enums.Constants import CellColors, UIConfig


class CellView:
    def __init__(self, parent, cell: Cell, size=32, click_callback=None):
        """
        parent         → Tkinter-Container (z. B. Frame)
        cell           → Logik-Cell
        size           → Pixelgröße
        click_callback → Funktion, die bei Klick ausgeführt wird (x, y übergeben)
        """
        self.cell = cell
        self.size = size
        self.click_callback = click_callback

        self.button = tk.Button(
            parent,
            width=size // UIConfig.CELL_SIZE_DIVISOR,
            height=size // (UIConfig.CELL_SIZE_DIVISOR * 2),
            command=self._on_click,
            borderwidth=0.5,
            highlightthickness=0,
            padx=0,
            pady=0
        )
        self.button.grid_propagate(False)

    def _on_click(self):
        if self.click_callback:
            self.click_callback(self.cell.x, self.cell.y)

    def set_enabled(self, enabled: bool):
        """Aktiviere/Deaktiviere die Interaktivität dieser Zelle."""
        self.button.config(state=("normal" if enabled else "disabled"))

    def update(self, highlight=False, highlight_invalid=False, ship_hover=False, ship_selected=False, 
               hide_ships_mines=False):
        """
        highlight: True, wenn diese Zelle beim Hover hervorgehoben werden soll (gültig)
        highlight_invalid: True, wenn diese Zelle beim Hover hervorgehoben werden soll (ungültig)
        ship_hover: True, wenn über ein Schiff gehovered wird (blau)
        ship_selected: True, wenn ein Schiff ausgewählt ist (grün)
        hide_ships_mines: True if ships and mines should be hidden on this board (default: False)
        """
        # Order: Invalid Hover > Ship Selected > Ship Hover > Valid Hover > Hit > Ship > Default
        if highlight_invalid and not hide_ships_mines:
            self.button.config(bg=CellColors.INVALID_HIGHLIGHT, text="")
            return
        if ship_selected and not hide_ships_mines:
            self.button.config(bg=CellColors.SHIP_SELECTED, text="")  # Green for selected ship
            return
        if ship_hover and not hide_ships_mines:
            self.button.config(bg=CellColors.SHIP_HOVER, text="")  # Blue for hover over ship
            return
        if highlight and not hide_ships_mines:
            self.button.config(bg=CellColors.VALID_HIGHLIGHT, text="")
            return

        # match/case on the display state provided by Cell
        match self.cell.state:
            case CellState.HIT_SHIP:
                self.button.config(text="", bg=CellColors.HIT_SHIP)
            case CellState.HIT_MINE:
                self.button.config(text="💣", bg=CellColors.HIT_MINE, fg="white")
            case CellState.MISS:
                self.button.config(text="", bg=CellColors.MISS)
            case CellState.SHIP:
                if hide_ships_mines:
                    self.button.config(text="", bg=CellColors.EMPTY)
                else:
                    self.button.config(text="", bg=CellColors.SHIP)
            case CellState.MINE:
                if hide_ships_mines:
                    self.button.config(text="", bg=CellColors.EMPTY)
                else:
                    self.button.config(text="", bg=CellColors.MINE)
            case CellState.EMPTY:
                self.button.config(text="", bg=CellColors.EMPTY)
