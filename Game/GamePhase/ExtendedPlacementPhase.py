from Game.GamePhase.PlacementPhase import PlacementPhase
from Objects.Mine import Mine
from Player.Player import Player
from Utils.Orientation import Orientation


class ExtendedPlacementPhase(PlacementPhase):
    def __init__(self, player1: Player, player2: Player, turn_callback, settings=None):
        super().__init__(player1, player2, turn_callback, settings)

    def create_game_objects(self, orientation):
        base = super().create_game_objects(Orientation.HORIZONTAL)
        base.extend([Mine(), Mine(), Mine()])
        return base