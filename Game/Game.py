from Utils.GameState import GameState
from Player.Player import Player


class Game:
    """
    Kapselt den Spielzustand und die Spiellogik für zwei Spieler.

    Attribute:
        players (list[Player]): Liste der beiden Spieler (Reihenfolge entspricht Zugreihenfolge).
        current_player_idx (int): Index des aktuellen Spielers (0 oder 1).
        current_state (GameState): Aktueller Spielzustand (PreStart, Placement, Shooting).
        settings: Einstellungen/Settings-Objekt mit UI-Auswahl (optional).
    """
    def __init__(self, player1: Player, player2: Player, settings=None):
        """Initialisiert ein Spiel mit zwei Spielern und optionalen Einstellungen.

        Args:
            player1 (Player): Spieler 1.
            player2 (Player): Spieler 2.
            settings: Optionales Settings-Objekt (z. B. aus der UI).
        """
        self.players = [player1, player2]
        self.current_player_idx = 0
        self.current_state = GameState.PreStart
        self.settings = settings

        # Setze game_objects in Settings, falls übergeben
        if settings is not None:
            from Utils.Orientation import Orientation
            import copy
            # Erzeuge die game_objects über die Factory-Methode
            base_objects = self.create_game_objects(Orientation.HORIZONTAL)
            settings.game_objects = [copy.deepcopy(obj) for obj in base_objects]

    def create_game_objects(self, orientation):
        """Erzeugt die Standard-Spielobjekte (Schiffe) für eine gegebene Ausrichtung.

        Args:
            orientation: Ausrichtung der zu erzeugenden Objekte (Orientation.HORIZONTAL/VERTICAL).
        Returns:
            list: Liste der erzeugten Spielobjekte.
        """
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

    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_idx]

    @property
    def other_player(self) -> Player:
        return self.players[1 - self.current_player_idx]

    @property
    def game_over(self) -> bool:
        for player in self.players:
            if player.has_lost:
                return True
        return False