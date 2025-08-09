import tkinter as tk

from Board.Cell import Cell, CellState


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
            width=size // 10,
            height=size // 20,
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

    def update(self, highlight=False, highlight_invalid=False):
        """
        highlight: True, wenn diese Zelle beim Hover hervorgehoben werden soll (gültig)
        highlight_invalid: True, wenn diese Zelle beim Hover hervorgehoben werden soll (ungültig)
        """
        # Reihenfolge: Ungültiges Hover > Gültiges Hover > Treffer > Schiff > Standard
        # Reihenfolge: Ungültiges Hover > Gültiges Hover > Treffer > Schiff > Standard
        if highlight_invalid:
            self.button.config(bg="#ff5555", text="")
            return
        if highlight:
            self.button.config(bg="#b3e6ff", text="")
            return

        # match/case über den von Cell gelieferten Darstellungszustand
        match self.cell.state:
            case CellState.HIT_SHIP:
                self.button.config(text="", bg="red")
            case CellState.HIT_MINE:
                self.button.config(text="💣", bg="black", fg="white")
            case CellState.MISS:
                self.button.config(text="", bg="black")
            case CellState.SHIP:
                self.button.config(text="", bg="gray")
            case CellState.EMPTY:
                self.button.config(text="", bg="white")
