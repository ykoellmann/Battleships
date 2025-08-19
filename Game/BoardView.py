from Board.Board import Board
from Game.CellView import CellView
from constants import UIConfig
import tkinter as tk

class BoardView:
    """
    Visual representation of a game board using Tkinter widgets.
    
    This class handles the display and user interaction for game boards,
    including cell clicking, hover effects, and visual updates for different
    game states like highlighting and ship placement visualization.
    
    Attributes:
        board: Reference to the logic Board instance
        cell_size: Pixel size of each cell in the grid
        click_callback: Callback function for cell click events (x, y)
        hover_callback: Callback function for cell hover events (x, y, enter)
    """
    def __init__(self, parent, board = Board(), cell_size=UIConfig.DEFAULT_CELL_SIZE, click_callback=None, hover_callback=None):
        """
        Create a new BoardView instance for displaying game boards.

        Args:
            parent: Tkinter parent container widget
            board: Logic board instance (default: new Board())
            cell_size: Pixel size of each cell (default: UIConfig.DEFAULT_CELL_SIZE)
            click_callback: Callback function for cell clicks (default: None)
            hover_callback: Callback function for cell hover events (default: None)
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
        """
        Internal handler for cell click events.

        Args:
            x: Column index of the clicked cell
            y: Row index of the clicked cell
        """
        if self.click_callback:
            self.click_callback(x, y)

    def _on_cell_hover(self, x, y, enter):
        """
        Internal handler for cell hover events.

        Args:
            x: Column index of the hovered cell
            y: Row index of the hovered cell
            enter: True when mouse enters cell, False when mouse leaves
        """
        if not self._hover_enabled:
            return
        if self.hover_callback:
            self.hover_callback(x, y, enter)

    def update(self, highlight_cells=None, highlight_invalid_cells=None, ship_hover_cells=None, ship_selected_cells=None):
        """
        Update the visual representation of all cells in the board.

        Args:
            highlight_cells: Set of valid hover cell coordinates (default: None)
            highlight_invalid_cells: Set of invalid hover cell coordinates (default: None)
            ship_hover_cells: Set of ship hover cell coordinates (default: None)
            ship_selected_cells: Set of selected ship cell coordinates (default: None)
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
                    highlight_invalid=(xy in highlight_invalid_cells) if highlight_invalid_cells else False,
                    ship_hover=(xy in ship_hover_cells) if ship_hover_cells else False,
                    ship_selected=(xy in ship_selected_cells) if ship_selected_cells else False
                )

    def set_hover_enabled(self, enabled: bool):
        """
        Enable or disable hover highlighting for this board.

        Args:
            enabled: True to enable hover effects, False to disable
        """
        self._hover_enabled = enabled

    def set_enabled(self, enabled: bool):
        """
        Enable or disable all cells in this board for user interaction.

        Args:
            enabled: True to enable cell interactions, False to disable
        """
        for row in self.cells_ui:
            for cell_ui in row:
                cell_ui.set_enabled(enabled)

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)