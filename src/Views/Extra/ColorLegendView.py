import tkinter as tk
from src.Utils.Enums.Constants import CellColors, UIColors


class ColorLegendView:
    """
    Popup window that explains the meaning of different cell colors in the game grid.
    
    Shows a visual legend with colored examples and text explanations for all
    possible cell states including ships, mines, hits, misses, and highlights.
    Uses the same brown color scheme as the main application.
    
    Attributes:
        window: Tkinter Toplevel window
        parent_window: Reference to the parent window for centering
        is_open: Whether the legend window is currently open
    """
    
    def __init__(self, parent_window: tk.Tk):
        """
        Initialize the color legend window.
        
        Args:
            parent_window: Parent window to center the legend window on
        """
        self.parent_window = parent_window
        self.window: tk.Toplevel = None
        self.is_open = False
    
    def open_window(self):
        """
        Open the color legend window and display all cell state explanations.
        
        Creates a new window if none exists, or brings existing window to front.
        """
        if self.is_open and self.window and self.window.winfo_exists():
            # Window already exists, just bring it to front
            self.window.lift()
            self.window.focus_set()
            return
        
        # Create new legend window
        self.window = tk.Toplevel(self.parent_window)
        self.window.title("Farblegende - Zellzustände")
        self.window.iconbitmap("assets\\logo.ico")
        self.window.geometry("400x600")
        self.window.configure(bg=UIColors.WINDOW_BG)
        
        # Make window non-resizable for consistent layout
        self.window.resizable(False, False)
        
        # Center window relative to parent
        self._center_window()
        
        # Create main frame with brown background
        main_frame = tk.Frame(self.window, bg=UIColors.FRAME_BG, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title label
        title_label = tk.Label(
            main_frame, 
            text="Farblegende", 
            font=("Arial", 14, "bold"),
            bg=UIColors.FRAME_BG,
            fg=UIColors.BUTTON_FG
        )
        title_label.pack(pady=(0, 20))
        
        # Create legend entries
        legend_data = [
            ("Leeres Feld", CellColors.EMPTY, "Noch nicht beschossenes Wasser"),
            ("Schiff", CellColors.SHIP, "Platziertes Schiff auf dem Spielfeld"),
            ("Mine", CellColors.MINE, "Platzierte Mine (nur im erweiterten Modus)"),
            ("Treffer Schiff", CellColors.HIT_SHIP, "Getroffenes Schiff"),
            ("Treffer Mine", CellColors.HIT_MINE, "Getroffene Mine (💣)"),
            ("Fehlschuss", CellColors.MISS, "Ins Wasser geschossen"),
            ("", "", ""),  # Separator
            ("Gültiger Platz", CellColors.VALID_HIGHLIGHT, "Gültige Position für Platzierung"),
            ("Schiff-Hover", CellColors.SHIP_HOVER, "Mauszeiger über Schiff"),
            ("Schiff ausgewählt", CellColors.SHIP_SELECTED, "Ausgewähltes Schiff"),
            ("Ungültiger Platz", CellColors.INVALID_HIGHLIGHT, "Ungültige Position für Platzierung")
        ]
        
        for title, color, description in legend_data:
            if title == "":  # Separator
                separator_frame = tk.Frame(main_frame, height=2, bg=UIColors.BOARD_BORDER)
                separator_frame.pack(fill=tk.X, pady=10)
                continue
                
            self._create_legend_entry(main_frame, title, color, description)
        
        # Close button
        close_btn = tk.Button(
            main_frame,
            text="Schließen",
            command=self.close_window,
            bg=UIColors.BUTTON_BG,
            fg=UIColors.BUTTON_FG,
            activebackground=UIColors.BUTTON_ACTIVE_BG,
            font=("Arial", 10, "bold"),
            padx=20,
            pady=5
        )
        close_btn.pack(pady=(20, 0))
        
        # Handle window close event
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)
        
        self.is_open = True
    
    def _create_legend_entry(self, parent, title, color, description):
        """
        Create a single legend entry with color sample and text.
        
        Args:
            parent: Parent widget to add the entry to
            title: Title text for the legend entry
            color: Background color for the color sample
            description: Detailed description text
        """
        entry_frame = tk.Frame(parent, bg=UIColors.FRAME_BG)
        entry_frame.pack(fill=tk.X, pady=2)
        
        # Color sample (small square showing the actual color)
        color_sample = tk.Label(
            entry_frame,
            text="💣" if title == "Treffer Mine" else "",
            bg=color,
            fg="white" if title == "Treffer Mine" else "black",
            width=3,
            height=1,
            relief="solid",
            borderwidth=1
        )
        color_sample.pack(side=tk.LEFT, padx=(0, 10))
        
        # Text container
        text_frame = tk.Frame(entry_frame, bg=UIColors.FRAME_BG)
        text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Title text
        title_label = tk.Label(
            text_frame,
            text=title,
            bg=UIColors.FRAME_BG,
            fg=UIColors.BUTTON_FG,
            font=("Arial", 10, "bold"),
            anchor="w"
        )
        title_label.pack(anchor="w")
        
        # Description text
        desc_label = tk.Label(
            text_frame,
            text=description,
            bg=UIColors.FRAME_BG,
            fg=UIColors.BUTTON_FG,
            font=("Arial", 9),
            anchor="w"
        )
        desc_label.pack(anchor="w")
    
    def close_window(self):
        """Close the color legend window."""
        if self.window:
            self.window.destroy()
            self.window = None
        self.is_open = False
    
    def _center_window(self):
        """Center the legend window relative to the parent window."""
        if not self.parent_window:
            return
        
        # Get parent window position and size
        parent_x = self.parent_window.winfo_x()
        parent_y = self.parent_window.winfo_y()
        parent_width = self.parent_window.winfo_width()
        parent_height = self.parent_window.winfo_height()
        
        # Calculate center position
        window_width = 400
        window_height = 600
        
        center_x = parent_x + (parent_width // 2) - (window_width // 2)
        center_y = parent_y + (parent_height // 2) - (window_height // 2)
        
        # Ensure window stays within screen bounds
        center_x = max(0, center_x)
        center_y = max(0, center_y)
        
        self.window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")