"""
Constants and enums for the Battleships game.

This module centralizes all magic strings, numbers, and configuration values
to improve maintainability and reduce code duplication.
"""

from enum import Enum


class GameMode(Enum):
    """Game mode options for standard vs extended gameplay."""
    STANDARD = "Standard"
    EXTENDED = "Erweitert"


class PlayerType(Enum):
    """Player type options for human vs computer players."""
    HUMAN = "Mensch"
    COMPUTER = "Computer"


class Difficulty(Enum):
    """Difficulty levels for computer players."""
    EASY = "Leicht"
    HARD = "Schwer"
    IMPOSSIBLE = "Unmöglich"


class ButtonType(Enum):
    """UI button types for game phase controls."""
    ORIENTATION = "orientation"
    CONFIRMATION = "confirmation"
    NONE = "none"


class BoardConfig:
    """Configuration constants for game boards."""
    DEFAULT_WIDTH = 10
    DEFAULT_HEIGHT = 10


class UIConfig:
    """Configuration constants for the user interface."""
    DEFAULT_PADDING = 10
    DEFAULT_CELL_SIZE = 32
    CELL_SIZE_DIVISOR = 10
    COMPUTER_TURN_DELAY_MS = 1000
    BUTTON_ROW_ORIENTATION = 3
    BUTTON_ROW_AUTO_PLACE = 4
    DEFAULT_PADY = 5


class CellColors:
    """Color constants for cell highlighting and states."""
    # Highlighting colors (priority order: invalid > selected > hover > valid)
    INVALID_HIGHLIGHT = "#ff5555"  # Red for invalid placement
    SHIP_SELECTED = "#00ff00"      # Green for selected ship
    SHIP_HOVER = "#0080ff"         # Blue for ship hover
    VALID_HIGHLIGHT = "#b3e6ff"    # Light blue for valid placement
    
    # Cell state colors
    HIT_SHIP = "red"               # Hit ship cell
    HIT_MINE = "black"             # Hit mine cell
    MISS = "black"                 # Miss cell
    SHIP = "gray"                  # Ship cell
    MINE = "orange"                # Mine cell
    EMPTY = "white"                # Empty cell


class GameConstants:
    """Centralized game configuration constants."""
    # Option lists for UI dropdowns
    DIFFICULTY_OPTIONS = [Difficulty.EASY.value, Difficulty.HARD.value, Difficulty.IMPOSSIBLE.value]
    PLAYER_TYPE_OPTIONS = [PlayerType.HUMAN.value, PlayerType.COMPUTER.value]
    GAME_MODE_OPTIONS = [GameMode.STANDARD.value, GameMode.EXTENDED.value]
    
    # Default player names
    DEFAULT_PLAYER1_NAME = "Spieler 1"
    DEFAULT_PLAYER2_NAME = "Spieler 2"
    
    # Default game settings
    DEFAULT_PLAYER1_TYPE = PlayerType.HUMAN.value
    DEFAULT_PLAYER2_TYPE = PlayerType.COMPUTER.value
    DEFAULT_PLAYER1_DIFFICULTY = Difficulty.EASY.value
    DEFAULT_PLAYER2_DIFFICULTY = Difficulty.EASY.value
    DEFAULT_GAME_MODE = GameMode.STANDARD.value


class MessageConstants:
    """Constants for user messages and dialog texts."""
    INVALID_PLACEMENT = "Ungültige Platzierung"
    INVALID_PLACEMENT_MESSAGE = "Hier kann das Schiff nicht platziert werden!"
    GAME_START = "Spielstart"
    GAME_START_MESSAGE = "Alle Schiffe platziert! Das Spiel beginnt."
    GAME_END = "Spielende"
    AUTO_PLACE_FAILED = "Auto-Platzierung fehlgeschlagen"
    AUTO_PLACE_FAILED_MESSAGE = "Nicht alle Schiffe konnten automatisch platziert werden!"


class ButtonLabels:
    """Constants for button labels and UI text."""
    TOGGLE_ORIENTATION = "Ausrichtung wechseln"
    CONFIRM_SELECTION = "Auswahl bestätigen"
    AUTO_PLACE_ALL = "Alle Schiffe automatisch platzieren"
    START_GAME = "Spiel starten"
    
    # UI labels
    GAME_SETTINGS = "Spiel-Einstellungen"
    PLAYER_1 = "Spieler 1:"
    PLAYER_2 = "Spieler 2:"
    GAME_MODE = "Spielmodus:"
    NORMAL = "Normal"
    EXTENDED = "Erweitert"
    GAME_ENDED = "Spiel beendet"