import tkinter as tk

from src.Core.Board.Cell import Cell, CellState
from src.Utils.Constants import CellColors, UIConfig


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
            padx=0,  # Kein horizontales Padding
            pady=0   # Kein vertikales Padding
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
        # Reihenfolge: Ungültiges Hover > Ship Selected > Ship Hover > Gültiges Hover > Treffer > Schiff > Standard
        if highlight_invalid:
            self.button.config(bg=CellColors.INVALID_HIGHLIGHT, text="")
            return
        if ship_selected:
            self.button.config(bg=CellColors.SHIP_SELECTED, text="")  # Grün für ausgewähltes Schiff
            return
        if ship_hover:
            self.button.config(bg=CellColors.SHIP_HOVER, text="")  # Blau für Hover über Schiff
            return
        if highlight:
            self.button.config(bg=CellColors.VALID_HIGHLIGHT, text="")
            return

        # match/case über den von Cell gelieferten Darstellungszustand
        match self.cell.state:
            case CellState.HIT_SHIP:
                self.button.config(text="", bg=CellColors.HIT_SHIP)
            case CellState.HIT_MINE:
                self.button.config(text="💣", bg=CellColors.HIT_MINE, fg="white")
            case CellState.MISS:
                self.button.config(text="", bg=CellColors.MISS)
            case CellState.SHIP:
                # Hide ships if requested by the visibility rules
                if hide_ships_mines:
                    self.button.config(text="", bg=CellColors.EMPTY)
                else:
                    self.button.config(text="", bg=CellColors.SHIP)
            case CellState.MINE:
                # Hide mines if requested by the visibility rules
                if hide_ships_mines:
                    self.button.config(text="", bg=CellColors.EMPTY)
                else:
                    self.button.config(text="", bg=CellColors.MINE)
            case CellState.EMPTY:
                self.button.config(text="", bg=CellColors.EMPTY)
