from Game.GamePhase.GamePhase import GamePhase
from Player.Computer.ComputerPlayer import ComputerPlayer
from Player.Computer.HardComputerPlayer import HardComputerPlayer
from Player.Player import Player
from Utils.GameState import GameState

class ShootingPhase(GamePhase):

    def __init__(self, player1: Player, player2: Player, turn_callback, settings=None):
        super().__init__(GameState.Shooting, player1, player2, turn_callback)

    def handle_cell_click(self, x, y):
        cell = self.other_player.board.get_cell(x, y)
        if cell.is_hit or cell.is_miss:
            return

        self.execute_turn(x, y)

    def execute_turn(self, x, y):
        result = self.other_player.board.shoot_at(x, y)

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
            self.turn_callback(hit, self.is_over())
            return


        if isinstance(self.current_player, ComputerPlayer):
            self.execute_computer_turn()

        self.turn_callback(hit, self.is_over())

    def is_over(self):
        return self.game_over

    def execute_computer_turn(self):
        target = self.current_player.select_target()
        x, y = target
        # comp_hit, _ = self.execute_turn(x, y)
        self.window.after(1000, lambda: self.execute_turn(x, y))



