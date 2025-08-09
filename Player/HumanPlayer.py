from Player.Player import Player


class HumanPlayer(Player):
    def __init__(self, name: str, board):
        super().__init__(name, board)

    def place_object(self, game_object):
        if self.board.can_place_object(game_object):
            self.objects.append(game_object)
            self.board.place_object(game_object)
