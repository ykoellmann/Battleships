from src.Utils.GameLogger import GameLogger
from src.Core.Game.Phases.EndPhase import EndPhase
from src.Core.Game.Phases.GamePhase import GamePhase
from src.Core.Game.Phases.PhaseConfig import PhaseConfig
from src.Players.Computer.ComputerPlayer import ComputerPlayer
from src.Players.Computer.HardComputerPlayer import HardComputerPlayer


class ShootingPhase(GamePhase):

    def __init__(self, config: PhaseConfig):
        """
        Initialize the ShootingPhase with configuration.
        
        This phase handles the shooting mechanics of the game.
        
        Args:
            config: PhaseConfig object containing all initialization parameters
        """
        super().__init__(config)

    def handle_cell_click(self, x, y, is_own_board):
        if is_own_board:
            return
        cell = self.other_player.board.get_cell(x, y)
        if cell.is_hit or cell.is_miss:
            return

        self.execute_turn(x, y)

    def execute_turn(self, x, y):
        result = self.other_player.board.shoot_at(x, y)
        
        # Log shooting attempt
        GameLogger.log_shot(
            self.current_player.name,
            x, y,
            result.hit,
            result.hit_object,
            result.is_destroyed
        )

        if isinstance(self.current_player, HardComputerPlayer):
            self.current_player.process_shot_result(
                x, y, result.hit, result.is_destroyed,
                result.hit_object.coordinates if result.hit_object else []
            )

        return result.hit, self.next_turn(result.hit)

    def next_turn(self, hit):
        if not hit:
            self.next_player()
        if self.is_over():
            self.next_phase()
            return

        if isinstance(self.current_player, ComputerPlayer):
            self.execute_computer_turn()

        self.turn_callback(hit, self.is_over())

    def is_over(self):
        return self.game_over

    def next_phase(self):
        new_phase = EndPhase
        self.next_phase_callback(new_phase)

    def execute_computer_turn(self):
        target = self.current_player.select_target()
        x, y = target
        # comp_hit, _ = self.execute_turn(x, y)
        self.window.after(1000, lambda: self.execute_turn(x, y))



