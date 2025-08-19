"""
Statistics window for displaying player behavior analytics.

This module provides a window that displays player statistics including
placement and shot heatmaps, total counts, and favorite positions.
"""

import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Tuple, Optional
import sqlite3

from src.Utils.Constants import UIColors
from src.Utils.Database.DatabaseManager import DatabaseManager
from src.Utils.Database.Placement.UserPlacementRepository import UserPlacementRepository
from src.Utils.Database.Shot.UserShotRepository import UserShotRepository


class StatisticsWindow:
    """
    Statistics window for displaying player behavior analytics.
    
    Shows player-specific statistics including placement and shot heatmaps,
    total activity counts, and favorite positions. Uses the same brown color
    scheme as the main application.
    
    Attributes:
        window: Tkinter Toplevel window
        parent_window: Reference to the parent window for centering
        is_open: Whether the statistics window is currently open
        db_manager: DatabaseManager instance for database access
        placement_repo: Repository for placement operations
        shot_repo: Repository for shot operations
        current_player: Currently selected player name
        placement_heatmap: Current player's placement heatmap data
        shot_heatmap: Current player's shot heatmap data
    """
    
    def __init__(self, parent_window: tk.Tk):
        """
        Initialize the statistics window.
        
        Args:
            parent_window: Parent window to center the statistics window on
        """
        self.parent_window = parent_window
        self.window: tk.Toplevel = None
        self.is_open = False
        
        # Initialize database access
        self.db_manager = DatabaseManager()
        self.placement_repo = UserPlacementRepository(self.db_manager.db_path)
        self.shot_repo = UserShotRepository(self.db_manager.db_path)
        
        # Current state
        self.current_player: Optional[str] = None
        self.placement_heatmap: Dict[Tuple[int, int], int] = {}
        self.shot_heatmap: Dict[Tuple[int, int], int] = {}
        
        # UI components
        self.player_combobox: ttk.Combobox = None
        self.placement_canvas: tk.Canvas = None
        self.shot_canvas: tk.Canvas = None
        self.stats_frame: tk.Frame = None
    
    def open_window(self):
        """
        Open the statistics window and display player analytics.
        
        Creates a new window if none exists, or brings existing window to front.
        """
        if self.is_open and self.window and self.window.winfo_exists():
            # Window already exists, just bring it to front
            self.window.lift()
            self.window.focus_set()
            return
        
        # Create new statistics window
        self.window = tk.Toplevel(self.parent_window)
        self.window.title("Spieler-Statistiken")
        self.window.geometry("1000x700")
        self.window.configure(bg=UIColors.WINDOW_BG)
        
        # Make window non-resizable for consistent layout
        self.window.resizable(False, False)
        
        # Center window relative to parent
        self._center_window()
        
        # Create main frame with brown background
        main_frame = tk.Frame(self.window, bg=UIColors.FRAME_BG, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create UI components
        self._create_header(main_frame)
        self._create_player_selection(main_frame)
        self._create_heatmap_section(main_frame)
        self._create_statistics_section(main_frame)
        self._create_controls(main_frame)
        
        # Handle window close event
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)
        
        # Load initial data
        self._refresh_player_list()
        
        self.is_open = True
    
    def _create_header(self, parent):
        """
        Create the header section with title.
        
        Args:
            parent: Parent widget to add the header to
        """
        title_label = tk.Label(
            parent, 
            text="Spieler-Statistiken", 
            font=("Arial", 16, "bold"),
            bg=UIColors.FRAME_BG,
            fg=UIColors.BUTTON_FG
        )
        title_label.pack(pady=(0, 20))
    
    def _create_player_selection(self, parent):
        """
        Create the player selection dropdown.
        
        Args:
            parent: Parent widget to add the selection to
        """
        selection_frame = tk.Frame(parent, bg=UIColors.FRAME_BG)
        selection_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Player selection label
        player_label = tk.Label(
            selection_frame,
            text="Spieler auswählen:",
            font=("Arial", 12, "bold"),
            bg=UIColors.FRAME_BG,
            fg=UIColors.BUTTON_FG
        )
        player_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Player selection dropdown
        self.player_combobox = ttk.Combobox(
            selection_frame,
            state="readonly",
            font=("Arial", 10),
            width=20
        )
        self.player_combobox.pack(side=tk.LEFT, padx=(0, 10))
        self.player_combobox.bind('<<ComboboxSelected>>', self._on_player_selected)
        
        # Refresh button
        refresh_btn = tk.Button(
            selection_frame,
            text="Aktualisieren",
            command=self._refresh_player_list,
            bg=UIColors.BUTTON_BG,
            fg=UIColors.BUTTON_FG,
            activebackground=UIColors.BUTTON_ACTIVE_BG,
            font=("Arial", 10),
            padx=10,
            pady=2
        )
        refresh_btn.pack(side=tk.LEFT)
    
    def _create_heatmap_section(self, parent):
        """
        Create the heatmap visualization section.
        
        Args:
            parent: Parent widget to add the heatmaps to
        """
        heatmap_frame = tk.Frame(parent, bg=UIColors.FRAME_BG)
        heatmap_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Left side - Placement heatmap
        placement_frame = tk.Frame(heatmap_frame, bg=UIColors.FRAME_BG)
        placement_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        placement_title = tk.Label(
            placement_frame,
            text="Platzierungen",
            font=("Arial", 12, "bold"),
            bg=UIColors.FRAME_BG,
            fg=UIColors.BUTTON_FG
        )
        placement_title.pack(pady=(0, 10))
        
        self.placement_canvas = tk.Canvas(
            placement_frame,
            width=320,
            height=320,
            bg="white",
            relief="solid",
            borderwidth=2
        )
        self.placement_canvas.pack()
        
        # Right side - Shot heatmap
        shot_frame = tk.Frame(heatmap_frame, bg=UIColors.FRAME_BG)
        shot_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        shot_title = tk.Label(
            shot_frame,
            text="Schüsse",
            font=("Arial", 12, "bold"),
            bg=UIColors.FRAME_BG,
            fg=UIColors.BUTTON_FG
        )
        shot_title.pack(pady=(0, 10))
        
        self.shot_canvas = tk.Canvas(
            shot_frame,
            width=320,
            height=320,
            bg="white",
            relief="solid",
            borderwidth=2
        )
        self.shot_canvas.pack()
    
    def _create_statistics_section(self, parent):
        """
        Create the statistics display section.
        
        Args:
            parent: Parent widget to add the statistics to
        """
        self.stats_frame = tk.Frame(parent, bg=UIColors.FRAME_BG)
        self.stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        stats_title = tk.Label(
            self.stats_frame,
            text="Statistiken",
            font=("Arial", 12, "bold"),
            bg=UIColors.FRAME_BG,
            fg=UIColors.BUTTON_FG
        )
        stats_title.pack(pady=(0, 10))
        
        # This will be populated when a player is selected
    
    def _create_controls(self, parent):
        """
        Create the control buttons.
        
        Args:
            parent: Parent widget to add the controls to
        """
        controls_frame = tk.Frame(parent, bg=UIColors.FRAME_BG)
        controls_frame.pack(fill=tk.X)
        
        # Close button
        close_btn = tk.Button(
            controls_frame,
            text="Schließen",
            command=self.close_window,
            bg=UIColors.BUTTON_BG,
            fg=UIColors.BUTTON_FG,
            activebackground=UIColors.BUTTON_ACTIVE_BG,
            font=("Arial", 10, "bold"),
            padx=20,
            pady=5
        )
        close_btn.pack(side=tk.RIGHT)
    
    def _refresh_player_list(self):
        """Refresh the list of available players from the database."""
        try:
            # Get all unique player names from both tables
            with sqlite3.connect(self.db_manager.db_path) as conn:
                cursor = conn.cursor()
                
                # Get players who have placements
                cursor.execute("SELECT DISTINCT player_name FROM user_placements")
                placement_players = set(row[0] for row in cursor.fetchall())
                
                # Get players who have shots
                cursor.execute("SELECT DISTINCT player_name FROM user_shots")
                shot_players = set(row[0] for row in cursor.fetchall())
                
                # Combine all players
                all_players = sorted(placement_players | shot_players)
                
                # Update combobox
                self.player_combobox['values'] = all_players
                
                if all_players and not self.current_player:
                    self.player_combobox.set(all_players[0])
                    self._on_player_selected(None)
                elif not all_players:
                    self.player_combobox.set("")
                    self._clear_display()
                    
        except Exception as e:
            print(f"Error refreshing player list: {e}")
            self.player_combobox['values'] = []
            self._clear_display()
    
    def _on_player_selected(self, event):
        """
        Handle player selection change.
        
        Args:
            event: The combobox selection event
        """
        selected_player = self.player_combobox.get()
        if selected_player and selected_player != self.current_player:
            self.current_player = selected_player
            self._load_player_data()
            self._update_display()
    
    def _load_player_data(self):
        """Load data for the currently selected player."""
        if not self.current_player:
            return
        
        try:
            # Get placement heatmap for current player
            self.placement_heatmap = self._get_player_placement_heatmap(self.current_player)
            
            # Get shot heatmap for current player
            self.shot_heatmap = self._get_player_shot_heatmap(self.current_player)
            
        except Exception as e:
            print(f"Error loading player data: {e}")
            self.placement_heatmap = {}
            self.shot_heatmap = {}
    
    def _get_player_placement_heatmap(self, player_name: str) -> Dict[Tuple[int, int], int]:
        """Get placement heatmap for a specific player."""
        with sqlite3.connect(self.db_manager.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT x, y, COUNT(*) as frequency
                FROM user_placements
                WHERE player_name = ?
                GROUP BY x, y
            """, (player_name,))
            result = cursor.fetchall()
        
        return {(x, y): frequency for x, y, frequency in result}
    
    def _get_player_shot_heatmap(self, player_name: str) -> Dict[Tuple[int, int], int]:
        """Get shot heatmap for a specific player."""
        with sqlite3.connect(self.db_manager.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT x, y, COUNT(*) as frequency
                FROM user_shots
                WHERE player_name = ?
                GROUP BY x, y
            """, (player_name,))
            result = cursor.fetchall()
        
        return {(x, y): frequency for x, y, frequency in result}
    
    def _update_display(self):
        """Update all display components with current player data."""
        self._draw_heatmap(self.placement_canvas, self.placement_heatmap)
        self._draw_heatmap(self.shot_canvas, self.shot_heatmap)
        self._update_statistics()
    
    def _draw_heatmap(self, canvas: tk.Canvas, heatmap_data: Dict[Tuple[int, int], int]):
        """
        Draw a heatmap on the specified canvas.
        
        Args:
            canvas: Canvas to draw on
            heatmap_data: Dictionary mapping coordinates to frequency
        """
        canvas.delete("all")
        
        if not heatmap_data:
            # Show empty message
            canvas.create_text(
                160, 160,
                text="Keine Daten verfügbar",
                font=("Arial", 12),
                fill="gray"
            )
            return
        
        # Calculate cell size (assuming 10x10 grid)
        cell_size = 30
        grid_size = 10
        
        # Find max frequency for color scaling
        max_frequency = max(heatmap_data.values()) if heatmap_data else 1
        
        # Draw grid
        for x in range(grid_size):
            for y in range(grid_size):
                x1 = x * cell_size + 10
                y1 = y * cell_size + 10
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                
                # Get frequency for this cell
                frequency = heatmap_data.get((x, y), 0)
                
                # Calculate color intensity based on frequency
                if frequency > 0:
                    intensity = frequency / max_frequency
                    # Create heat color (white to red)
                    red = int(255)
                    green = int(255 * (1 - intensity))
                    blue = int(255 * (1 - intensity))
                    color = f"#{red:02x}{green:02x}{blue:02x}"
                else:
                    color = "white"
                
                # Draw cell
                canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline="black",
                    width=1
                )
                
                # Draw frequency text if > 0
                if frequency > 0:
                    canvas.create_text(
                        x1 + cell_size/2, y1 + cell_size/2,
                        text=str(frequency),
                        font=("Arial", 8, "bold"),
                        fill="black"
                    )
        
        # Draw grid labels
        for i in range(grid_size):
            # X-axis labels (top)
            canvas.create_text(
                i * cell_size + 10 + cell_size/2, 5,
                text=str(i),
                font=("Arial", 8),
                fill="black"
            )
            # Y-axis labels (left)
            canvas.create_text(
                5, i * cell_size + 10 + cell_size/2,
                text=str(i),
                font=("Arial", 8),
                fill="black"
            )
    
    def _update_statistics(self):
        """Update the statistics display section."""
        # Clear existing statistics
        for widget in self.stats_frame.winfo_children():
            if widget.winfo_class() != 'Label' or widget.cget('text') != 'Statistiken':
                widget.destroy()
        
        if not self.current_player:
            return
        
        try:
            # Get total counts for current player
            with sqlite3.connect(self.db_manager.db_path) as conn:
                cursor = conn.cursor()
                
                # Total placements
                cursor.execute(
                    "SELECT COUNT(*) FROM user_placements WHERE player_name = ?",
                    (self.current_player,)
                )
                total_placements = cursor.fetchone()[0]
                
                # Total shots
                cursor.execute(
                    "SELECT COUNT(*) FROM user_shots WHERE player_name = ?",
                    (self.current_player,)
                )
                total_shots = cursor.fetchone()[0]
            
            # Create statistics display
            stats_info_frame = tk.Frame(self.stats_frame, bg=UIColors.FRAME_BG)
            stats_info_frame.pack(fill=tk.X)
            
            # Left column
            left_stats = tk.Frame(stats_info_frame, bg=UIColors.FRAME_BG)
            left_stats.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            tk.Label(
                left_stats,
                text=f"Gesamte Platzierungen: {total_placements}",
                font=("Arial", 11),
                bg=UIColors.FRAME_BG,
                fg=UIColors.BUTTON_FG,
                anchor="w"
            ).pack(fill=tk.X, pady=2)
            
            tk.Label(
                left_stats,
                text=f"Gesamte Schüsse: {total_shots}",
                font=("Arial", 11),
                bg=UIColors.FRAME_BG,
                fg=UIColors.BUTTON_FG,
                anchor="w"
            ).pack(fill=tk.X, pady=2)
            
            # Right column - Favorite positions
            right_stats = tk.Frame(stats_info_frame, bg=UIColors.FRAME_BG)
            right_stats.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 0))
            
            # Most frequent placement position
            if self.placement_heatmap:
                max_placement_pos = max(self.placement_heatmap, key=self.placement_heatmap.get)
                max_placement_freq = self.placement_heatmap[max_placement_pos]
                tk.Label(
                    right_stats,
                    text=f"Lieblings-Platzierung: ({max_placement_pos[0]},{max_placement_pos[1]}) - {max_placement_freq}x",
                    font=("Arial", 11),
                    bg=UIColors.FRAME_BG,
                    fg=UIColors.BUTTON_FG,
                    anchor="w"
                ).pack(fill=tk.X, pady=2)
            
            # Most frequent shot position
            if self.shot_heatmap:
                max_shot_pos = max(self.shot_heatmap, key=self.shot_heatmap.get)
                max_shot_freq = self.shot_heatmap[max_shot_pos]
                tk.Label(
                    right_stats,
                    text=f"Lieblings-Schuss: ({max_shot_pos[0]},{max_shot_pos[1]}) - {max_shot_freq}x",
                    font=("Arial", 11),
                    bg=UIColors.FRAME_BG,
                    fg=UIColors.BUTTON_FG,
                    anchor="w"
                ).pack(fill=tk.X, pady=2)
            
        except Exception as e:
            print(f"Error updating statistics: {e}")
    
    def _clear_display(self):
        """Clear all display components."""
        if self.placement_canvas:
            self.placement_canvas.delete("all")
        if self.shot_canvas:
            self.shot_canvas.delete("all")
        
        # Clear statistics
        for widget in self.stats_frame.winfo_children():
            if widget.winfo_class() != 'Label' or widget.cget('text') != 'Statistiken':
                widget.destroy()
        
        self.current_player = None
        self.placement_heatmap = {}
        self.shot_heatmap = {}
    
    def close_window(self):
        """Close the statistics window."""
        if self.window:
            self.window.destroy()
            self.window = None
        self.is_open = False
    
    def _center_window(self):
        """Center the statistics window relative to the parent window."""
        if not self.parent_window:
            return
        
        # Get parent window position and size
        parent_x = self.parent_window.winfo_x()
        parent_y = self.parent_window.winfo_y()
        parent_width = self.parent_window.winfo_width()
        parent_height = self.parent_window.winfo_height()
        
        # Calculate center position
        window_width = 1000
        window_height = 700
        
        center_x = parent_x + (parent_width // 2) - (window_width // 2)
        center_y = parent_y + (parent_height // 2) - (window_height // 2)
        
        # Ensure window stays within screen bounds
        center_x = max(0, center_x)
        center_y = max(0, center_y)
        
        self.window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")