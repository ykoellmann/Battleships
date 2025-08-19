from typing import Union

from constants import PlayerType, Difficulty
from Models.PlayerConfig import PlayerConfig
from Player.Computer.EasyComputerPlayer import EasyComputerPlayer
from Player.Computer.HardComputerPlayer import HardComputerPlayer
from Player.Computer.ImpossibleComputerPlayer import ImpossibleComputerPlayer
from Player.HumanPlayer import HumanPlayer
from Player.Player import Player


class PlayerFactory:
    """
    Factory class for creating player instances.
    
    This factory provides a centralized way to create different types of players
    (human and computer with various difficulty levels) using configuration objects
    or direct parameters. Uses enum constants for type safety and consistency.
    """
    
    _computer_map = {
        Difficulty.EASY.value: lambda board, opponent_board, name: EasyComputerPlayer(board),
        Difficulty.HARD.value: lambda board, opponent_board, name: HardComputerPlayer(board),
        Difficulty.IMPOSSIBLE.value: lambda board, opponent_board, name: ImpossibleComputerPlayer(board, opponent_board),
    }

    @staticmethod
    def create(player_type: str, player_name: str, level: str, board, opponent_board) -> Player:
        """
        Create a player instance based on type and configuration.
        
        Args:
            player_type: Type of player (Human or Computer)
            player_name: Display name for the player
            level: Difficulty level for computer players
            board: Player's own game board
            opponent_board: Opponent's game board
            
        Returns:
            Player: Configured player instance
            
        Raises:
            ValueError: If player type or difficulty level is invalid
        """
        if player_type == PlayerType.HUMAN.value:
            return HumanPlayer(player_name, board)

        if player_type == PlayerType.COMPUTER.value and level in PlayerFactory._computer_map:
            return PlayerFactory._computer_map[level](board, opponent_board, player_name)

        raise ValueError(f"Invalid player type: {player_type}, Level: {level}")
    
    @staticmethod
    def create_from_config(config: PlayerConfig) -> Player:
        """
        Create a player instance from a PlayerConfig object.
        
        Args:
            config: PlayerConfig object containing all player parameters
            
        Returns:
            Player: Configured player instance
        """
        return PlayerFactory.create(
            config.player_type,
            config.name,
            config.difficulty,
            config.board,
            config.opponent_board
        )