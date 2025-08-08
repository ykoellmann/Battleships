from Objects.Ships.Battleship import Battleship
from Objects.Ships.Cruiser import Cruiser
from Objects.Ships.Destroyer import Destroyer
from Objects.Ships.Submarine import Submarine
from Objects.Utils.Orientation import Orientation
from Player.Player import Player
import tkinter as tk


class Game:
    def __init__(self, player1: Player, player2: Player):
        self.players = [player1, player2]
        self.current_player_idx = 0
        self.game_over = False

        # self.window = tk.Tk()
        # self.window.title("Schiffe versenken")

    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_idx]

    @property
    def other_player(self) -> Player:
        return self.players[1 - self.current_player_idx]

    def _place_initial_objects(self, player: Player):
        objects = [
            Battleship(Orientation.HORIZONTAL),  # 1x Schlachtschiff (5 Felder)
            Cruiser(Orientation.HORIZONTAL),  # 2x Kreuzer (4 Felder)
            Cruiser(Orientation.HORIZONTAL),
            Destroyer(Orientation.HORIZONTAL),  # 3x Zerstörer (3 Felder)
            Destroyer(Orientation.HORIZONTAL),
            Destroyer(Orientation.HORIZONTAL),
            Submarine(Orientation.HORIZONTAL),  # 4x U-Boot (2 Felder)
            Submarine(Orientation.HORIZONTAL),
            Submarine(Orientation.HORIZONTAL),
            Submarine(Orientation.HORIZONTAL)
        ]
        for obj in objects:
            player.place_object(obj)

    def make_turn(self, x: int, y: int) -> bool:
        # Spielzug durchführen
        hit = self.other_player.board.shoot(x, y)

        if not hit:
            # Bei Fehlschuss ist der andere Spieler dran
            self.current_player_idx = 1 - self.current_player_idx

        self._check_game_over()
        return hit

    def _check_game_over(self):
        # Prüfen ob alle Schiffe eines Spielers zerstört sind
        for player in self.players:
            if player.has_lost():
                self.game_over = True
                break