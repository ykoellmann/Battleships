import random

from Game.GamePhase.ShootingPhase import ShootingPhase
from Objects.Ships.Ship import Ship
from Player.Computer.ComputerPlayer import ComputerPlayer
from Player.Computer.HardComputerPlayer import HardComputerPlayer
from Player.Player import Player


class ExtendedShootingPhase(ShootingPhase):
    def __init__(self, player1: Player, player2: Player, turn_callback, settings=None):
        super().__init__(player1, player2, turn_callback)
        self.shooting_ship = None
        self.shot = 0

    def handle_cell_click(self, x, y, is_own_board):
        if not is_own_board:
            return super().handle_cell_click(x, y)

        clicked_object = self.current_player.board.get_cell(x,y).object

        self.new_shooting_ship(clicked_object)
        return

    def execute_turn(self, x, y):
        result = self.other_player.board.shoot_at(x, y)
        if self.shooting_ship:
            self.shot += 1

        if isinstance(self.current_player, HardComputerPlayer):
            self.current_player.process_shot_result(
                x, y, result.hit, result.is_destroyed,
                result.hit_object.coordinates if result.hit_object else []
            )

        return result.hit, self.next_turn(result.hit)

    def next_turn(self, hit):
        if (not self.shooting_ship) or self.shot >= self.shooting_ship.size:
            self.next_player()

        if isinstance(self.current_player, ComputerPlayer):
            self.execute_computer_turn()

        self.turn_callback(hit, self.is_over())

    def next_player(self):
        self.shooting_ship = None
        self.shot = 0
        super().next_player()


    def execute_computer_turn(self):
        target = self.current_player.select_target()

        random_objects = [obj for obj in self.current_player.objects if not obj.is_destroyed]
        if random_objects:
            random_object = random.choice(random_objects)
            self.new_shooting_ship(random_object)

        x, y = target
        # comp_hit, _ = self.execute_turn(x, y)
        self.window.after(1000, lambda: self.execute_turn(x, y))

    def new_shooting_ship(self, ship: Ship):
        if not (ship and isinstance(ship, Ship) and self.shot == 0):
            return
        self.shooting_ship = ship
        self.shot = 0