import copy
from Game.GamePhase.GamePhase import GamePhase
from Game.GamePhase.PhaseConfig import PhaseConfig
from Objects.GameObject import GameObject
from Player.Computer.ComputerPlayer import ComputerPlayer
from Player.HumanPlayer import HumanPlayer
from Player.Player import Player
from Utils.GameState import GameState
from Utils.Orientation import Orientation


class PlacementPhase(GamePhase):

    def __init__(self, config: PhaseConfig):
        """
        Initialize the PlacementPhase with configuration.
        
        This phase handles the placement of ships and other game objects on the board.
        
        Args:
            config: PhaseConfig object containing all initialization parameters
        """
        self.placement_object_idx = 0
        if config.settings is not None:
            base_objects = self.create_game_objects(Orientation.HORIZONTAL)
            config.settings.game_objects = [copy.deepcopy(obj) for obj in base_objects]
        super().__init__(config)

    def handle_cell_click(self, x, y, is_own_board):
        if not isinstance(self.current_player, HumanPlayer):
            return
        if not is_own_board:
            return

        is_placed = self.execute_turn(x, y)
        if is_placed:
            self.next_placement()
            self.next_turn()

    def next_turn(self):
        if self.is_over():
            self.turn_callback(True, True)
            return
        else:
            self.turn_callback(True, False)
        if not isinstance(self.current_player, ComputerPlayer):
            return

        self.execute_turn()
        self.next_placement()
        self.next_turn()

    def is_over(self):
        total = len(self.settings.game_objects)
        if self.placement_object_idx < total:
            return False

        self.placement_object_idx = 0
        if self.next_player():
            self.next_phase()
            return True
        return False  # oder True, wenn direkt Phasewechsel

    def next_phase(self):
        new_phase = PlacementPhase
        self.next_phase_callback(new_phase)

    @property
    def current_object(self) -> GameObject:
        return self.settings.game_objects[self.placement_object_idx]

    def execute_turn(self, x: int = -1, y: int = -1):
        obj_copy = copy.deepcopy(self.current_object)
        obj_copy.set_position(x, y)
        if not self.current_player.board.can_place_object(obj_copy):
            if not isinstance(self.current_player, ComputerPlayer):
                self.turn_callback(False, False)
                return False
        self.current_player.place_object(obj_copy)
        self.turn_callback(True, False)
        return True

    def next_placement(self):
        self.placement_object_idx += 1

    def toggle_orientation(self):
        self.current_object.rotate()

    def create_game_objects(self, orientation):
        from Objects.Ships.Battleship import Battleship
        from Objects.Ships.Cruiser import Cruiser
        from Objects.Ships.Destroyer import Destroyer
        from Objects.Ships.Submarine import Submarine
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