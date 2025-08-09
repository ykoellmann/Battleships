from Game.Game import Game
from Objects.Mine import Mine
from Player.Player import Player


class GameExtended(Game):
    def create_game_objects(self, orientation):
        # Hole die Standard-Schiffe und ergänze Minen
        objects = super().create_game_objects(orientation)
        objects.extend([Mine(), Mine(), Mine()])
        return objects
