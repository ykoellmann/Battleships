from Player.Computer.EasyComputerPlayer import EasyComputerPlayer
from Player.Computer.HardComputerPlayer import HardComputerPlayer
from Player.Computer.ImpossibleComputerPlayer import ImpossibleComputerPlayer
from Player.HumanPlayer import HumanPlayer


class PlayerFactory:
    _computer_map = {
        "leicht": lambda board, opponent_board, name: EasyComputerPlayer(board),
        "schwer": lambda board, opponent_board, name: HardComputerPlayer(board),
        "unmöglich": lambda board, opponent_board, name: ImpossibleComputerPlayer(board, opponent_board),
    }

    @staticmethod
    def create(player_type: str, player_name: str, level: str, board, opponent_board):
        player_type = (player_type or "").lower()
        level = (level or "").lower()

        if player_type == "mensch":
            return HumanPlayer(player_name, board)

        if player_type == "computer" and level in PlayerFactory._computer_map:
            return PlayerFactory._computer_map[level](board, opponent_board, player_name)

        raise ValueError(f"Unbekannter Spielertyp: {player_type}, Level: {level}")