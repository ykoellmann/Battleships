import tkinter as tk
from tkinter import scrolledtext
from src.Utils.GameLogger import GameLogger
from src.Utils.Enums.Constants import UIColors


class LogView:
    """
    Separate window for displaying game log entries.
    
    Shows timestamped log entries with player actions and results in a 
    scrollable text area. The window can be opened and closed independently
    of the main game window. Uses the static GameLogger class for log access.
    
    Attributes:
        window: Tkinter Toplevel window
        text_area: ScrolledText widget for displaying log entries
        is_open: Whether the log window is currently open
    """
    
    def __init__(self, parent_window: tk.Tk):
        """
        Initialize the log window.
        
        Args:
            parent_window: Parent window to center the log window on
        """
        self.parent_window = parent_window
        self.window: tk.Toplevel = None
        self.text_area: scrolledtext.ScrolledText = None
        self.is_open = False
    
    def open_window(self):
        """
        Open the log window and display current log entries.
        
        Creates a new window if none exists, or brings existing window to front.
        """
        if self.is_open and self.window and self.window.winfo_exists():
            self.window.lift()
            self.window.focus_set()
            self.refresh_log()
            return

        self.window = tk.Toplevel(self.parent_window)
        self.window.title("Spiel-Log")
        self.window.iconbitmap("assets\\logo.ico")
        self.window.geometry("600x400")
        self.window.configure(bg=UIColors.WINDOW_BG)

        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)

        self._center_window()

        main_frame = tk.Frame(self.window, bg=UIColors.FRAME_BG)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)

        title_label = tk.Label(main_frame, text="Spiel-Ereignisse", font=("Arial", 12, "bold"),
                              bg=UIColors.FRAME_BG, fg=UIColors.BUTTON_FG)
        title_label.grid(row=0, column=0, sticky="w", pady=(0, 10))

        self.text_area = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            width=70,
            height=20,
            font=("Consolas", 10),
            state=tk.DISABLED,
            bg=UIColors.BUTTON_BG,
            fg=UIColors.BUTTON_FG
        )
        self.text_area.grid(row=1, column=0, sticky="nsew")

        button_frame = tk.Frame(main_frame, bg=UIColors.FRAME_BG)
        button_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        button_frame.columnconfigure(0, weight=1)

        refresh_btn = tk.Button(button_frame, text="Aktualisieren", command=self.refresh_log,
                               bg=UIColors.BUTTON_BG, fg=UIColors.BUTTON_FG, activebackground=UIColors.BUTTON_ACTIVE_BG)
        refresh_btn.grid(row=0, column=0, sticky="w")

        clear_btn = tk.Button(button_frame, text="Log löschen", command=self.clear_log,
                             bg=UIColors.BUTTON_BG, fg=UIColors.BUTTON_FG, activebackground=UIColors.BUTTON_ACTIVE_BG)
        clear_btn.grid(row=0, column=1, sticky="w", padx=(10, 0))

        close_btn = tk.Button(button_frame, text="Schließen", command=self.close_window,
                             bg=UIColors.BUTTON_BG, fg=UIColors.BUTTON_FG, activebackground=UIColors.BUTTON_ACTIVE_BG)
        close_btn.grid(row=0, column=2, sticky="e")

        self.window.protocol("WM_DELETE_WINDOW", self.close_window)
        
        self.is_open = True
        self.refresh_log()

        # Auto-scroll to bottom
        self.text_area.see(tk.END)
    
    def close_window(self):
        """Close the log window."""
        if self.window:
            self.window.destroy()
            self.window = None
        self.is_open = False
    
    def refresh_log(self):
        """Refresh the log display with current entries."""
        if not self.text_area:
            return

        self.text_area.config(state=tk.NORMAL)

        self.text_area.delete(1.0, tk.END)

        log_text = GameLogger.get_log_text()
        if log_text:
            self.text_area.insert(tk.END, log_text)
        else:
            self.text_area.insert(tk.END, "Keine Ereignisse vorhanden.")
        
        # Disable text area to prevent user editing
        self.text_area.config(state=tk.DISABLED)

        # Auto-scroll to bottom
        self.text_area.see(tk.END)
    
    def clear_log(self):
        """Clear all log entries."""
        GameLogger.clear_log()
        self.refresh_log()
    
    def _center_window(self):
        """Center the log window relative to the parent window."""
        if not self.parent_window:
            return

        parent_x = self.parent_window.winfo_x()
        parent_y = self.parent_window.winfo_y()
        parent_width = self.parent_window.winfo_width()
        parent_height = self.parent_window.winfo_height()
        
        # Calculate center position
        window_width = 600
        window_height = 400
        
        center_x = parent_x + (parent_width // 2) - (window_width // 2)
        center_y = parent_y + (parent_height // 2) - (window_height // 2)
        
        # Ensure window stays within screen bounds
        center_x = max(0, center_x)
        center_y = max(0, center_y)
        
        self.window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    
    def update_log(self):
        """Update the log display if window is open."""
        if self.is_open and self.window and self.window.winfo_exists():
            self.refresh_log()