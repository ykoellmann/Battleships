import copy

from src.Utils.GameLogger import GameLogger
from src.Core.GamePhases.GamePhase import GamePhase
from src.Utils.Settings.PhaseConfig import PhaseConfig
from src.Players.Computer.ComputerPlayer import ComputerPlayer
from src.Players.HumanPlayer import HumanPlayer
from src.Utils.Enums.Orientation import Orientation
from src.Core.Entities.GameObject import GameObject


class PlacementPhase(GamePhase):
    """
    Game phase for placing ships and other game objects on player boards.
    
    This phase handles the sequential placement of all game objects (ships, mines)
    for both players. It supports both human player interaction and automatic
    computer player placement.
    
    Attributes:
        placement_object_idx (int): Index of the current object being placed
        All attributes inherited from GamePhase
    """

    def __init__(self, config: PhaseConfig) -> None:
        """
        Initialize the PlacementPhase with configuration.
        
        This phase handles the placement of ships and other game objects on the board.
        It creates the initial game objects if settings are provided.
        
        Args:
            config: PhaseConfig object containing all initialization parameters
        """
        self.placement_object_idx: int = 0
        if config.settings is not None:
            base_objects = self.create_game_objects(Orientation.HORIZONTAL)
            config.settings.game_objects = [copy.deepcopy(obj) for obj in base_objects]
        super().__init__(config)

    def handle_cell_click(self, x: int, y: int, is_own_board: bool) -> None:
        """
        Handle cell click events during placement phase.
        
        Only processes clicks from human players on their own board.
        Attempts to place the current object and advances if successful.
        
        Args:
            x: X coordinate of the clicked cell
            y: Y coordinate of the clicked cell
            is_own_board: True if clicking on own board, False for opponent board
        """
        if not isinstance(self.current_player, HumanPlayer):
            return
        if not is_own_board:
            return

        is_placed = self.execute_turn(x, y)
        if is_placed:
            self.next_placement()
            self.next_turn()

    def next_turn(self) -> None:
        """
        Advance to the next turn in the placement phase.
        
        Handles turn progression, callback notifications, and automatic
        placement for computer players.
        """
        if self.is_over():
            return
        else:
            self.turn_callback(True, False)
        if not isinstance(self.current_player, ComputerPlayer):
            return

        # Use the unified auto-placement method for computer players
        self.auto_place_all_ships()
        self.next_turn()

    def is_over(self) -> bool:
        """
        Check if the placement phase is complete.
        
        The phase is over when all objects have been placed for both players.
        Triggers phase transition when complete.
        
        Returns:
            bool: True if placement phase should end, False otherwise
        """
        total = len(self.settings.game_objects)
        if self.placement_object_idx < total:
            return False

        self.placement_object_idx = 0
        if self.next_player():
            self.next_phase()
            return True
        return False

    def next_phase(self) -> None:
        """
        Trigger transition to the shooting phase.
        
        Selects appropriate shooting phase based on game mode
        (standard or extended).
        """
        from src.Core.GamePhases.ShootingPhase import ShootingPhase
        from src.Core.GamePhases.Extended.ExtendedShootingPhase import ExtendedShootingPhase

        if self.settings.mode == "Erweitert":
            new_phase = ExtendedShootingPhase
        else:
            new_phase = ShootingPhase
        self.next_phase_callback(new_phase)

    @property
    def current_object(self) -> GameObject:
        """
        Get the current game object being placed.
        
        Returns:
            GameObject: The object that should be placed next
        """
        return self.settings.game_objects[self.placement_object_idx]

    def execute_turn(self, x: int = -1, y: int = -1) -> bool:
        """
        Execute a placement turn at the specified coordinates.
        
        Creates a copy of the current object, sets its position, and attempts
        to place it on the current player's board.
        
        Args:
            x: X coordinate for placement (default: -1)
            y: Y coordinate for placement (default: -1)
            
        Returns:
            bool: True if placement was successful, False otherwise
        """
        obj_copy = copy.deepcopy(self.current_object)
        obj_copy.set_position(x, y)
        
        can_place = self.current_player.board.can_place_object(obj_copy)
        
        GameLogger.log_ship_placement(
            self.current_player.name, 
            obj_copy, 
            x, y, 
            can_place
        )
        
        if not can_place:
            if not isinstance(self.current_player, ComputerPlayer):
                self.turn_callback(False, False)
                return False
        
        self.current_player.place_object(obj_copy)
        self.turn_callback(True, False)
        return True

    def next_placement(self) -> None:
        """
        Advance to the next object in the placement sequence.
        """
        self.placement_object_idx += 1

    def toggle_orientation(self) -> None:
        """
        Toggle the orientation of the current object being placed.
        
        This method rotates the current object between horizontal and vertical
        orientations for human player placement.
        """
        self.current_object.rotate()

    def auto_place_all_ships(self):
        """
        Automatically place all remaining ships for the current player.
        
        This method places all remaining ships using the same logic as ComputerPlayer,
        making it available for both human and computer players.
        
        Returns:
            bool: True if all ships were successfully placed, False otherwise
        """

        # Continue placing ships until all are placed for the current player
        while self.placement_object_idx < len(self.settings.game_objects):
            current_obj = copy.deepcopy(self.current_object)
            self.current_player.place_random(current_obj)
            self.next_placement()

        return True

    def create_game_objects(self, orientation):
        from src.Core.Entities.Ships.Battleship import Battleship
        from src.Core.Entities.Ships.Cruiser import Cruiser
        from src.Core.Entities.Ships.Destroyer import Destroyer
        from src.Core.Entities.Ships.Submarine import Submarine
        return [
            Battleship(orientation),
            Cruiser(orientation),
            Cruiser(orientation),
            Destroyer(orientation),
            Destroyer(orientation),
            Destroyer(orientation),
            Submarine(orientation),
            Submarine(orientation),
            Submarine(orientation),
            Submarine(orientation),
        ]
