from Board.Board import Board
from Game.CellView import CellView
import tkinter as tk

class BoardView:
    """Darstellung eines Boards (Raster) in Tkinter.

    Attribute:
        board: Referenz auf das Logik-Board.
        cell_size (int): Pixelgröße einer Zelle.
        click_callback (callable | None): Callback bei Klick auf eine Zelle (x, y).
        hover_callback (callable | None): Callback bei Hover über eine Zelle (x, y, enter).
    """
    def __init__(self, parent, board = Board(), cell_size=32, click_callback=None, hover_callback=None):
        """Erzeugt eine BoardView.

        Args:
            parent: Tkinter-Container/Elternelement.
            board: Logik-Board-Instanz.
            cell_size (int): Pixelgröße einer Zelle.
            click_callback (callable | None): Callback bei Klick (x, y).
            hover_callback (callable | None): Callback bei Hover (x, y, enter).
        """
        self.board = board
        self.cell_size = cell_size
        self.click_callback = click_callback
        self.hover_callback = hover_callback
        self._hover_enabled = False  # Hover im Pre-Game deaktiviert

        # Rahmen um das gesamte Feld, leicht grau
        self.frame = tk.Frame(parent, highlightbackground="#cccccc", highlightthickness=2, bd=0)
        self.cells_ui = []
        self._build_cells()

    def _build_cells(self):
        self.cells_ui.clear()
        for y in range(self.board.height):
            row_ui = []
            for x in range(self.board.width):
                cell = self.board.get_cell(x, y)
                cell_ui = CellView(
                    self.frame,
                    cell,
                    size=self.cell_size,
                    click_callback=self._on_cell_click
                )
                # Mouse-Events für Hover
                cell_ui.button.bind("<Enter>", lambda e, xx=x, yy=y: self._on_cell_hover(xx, yy, True))
                cell_ui.button.bind("<Leave>", lambda e, xx=x, yy=y: self._on_cell_hover(xx, yy, False))
                # Kein padding und kein interner Rand zwischen den Zellen
                cell_ui.button.grid(row=y, column=x)
                row_ui.append(cell_ui)
            self.cells_ui.append(row_ui)

    def _on_cell_click(self, x, y):
        """Interner Handler für Klicks auf Zellen.

        Args:
            x (int): Spaltenindex.
            y (int): Zeilenindex.
        """
        if self.click_callback:
            self.click_callback(x, y)

    def _on_cell_hover(self, x, y, enter):
        """Interner Handler für Hover-Ereignisse über Zellen.

        Args:
            x (int): Spaltenindex.
            y (int): Zeilenindex.
            enter (bool): True bei Enter, False bei Leave.
        """
        if not self._hover_enabled:
            return
        if self.hover_callback:
            self.hover_callback(x, y, enter)

    def update(self, highlight_cells=None, highlight_invalid_cells=None):
        """Aktualisiert die Darstellung der Zellen.

        Args:
            highlight_cells (set[tuple[int,int]] | None): Menge gültiger Hover-Zellen.
            highlight_invalid_cells (set[tuple[int,int]] | None): Menge ungültiger Hover-Zellen.
        """
        # Falls das Board gewechselt wurde, Zellen neu bauen
        if len(self.cells_ui) != self.board.height or len(self.cells_ui[0]) != self.board.width:
            self._build_cells()
        for row in self.cells_ui:
            for cell_ui in row:
                cell_ui.cell = self.board.get_cell(cell_ui.cell.x, cell_ui.cell.y)
                xy = (cell_ui.cell.x, cell_ui.cell.y)
                cell_ui.update(
                    highlight=(xy in highlight_cells) if highlight_cells else False,
                    highlight_invalid=(xy in highlight_invalid_cells) if highlight_invalid_cells else False
                )

    def set_hover_enabled(self, enabled: bool):
        """Aktiviert/Deaktiviert Hover-Markierungen.

        Args:
            enabled (bool): True, um Hover zu erlauben.
        """
        self._hover_enabled = enabled

    def set_enabled(self, enabled: bool):
        """Aktiviert/Deaktiviert alle Zellen dieses Boards."""
        for row in self.cells_ui:
            for cell_ui in row:
                cell_ui.set_enabled(enabled)

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)