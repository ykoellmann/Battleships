from src.Core.GamePhases.PlacementPhase import PlacementPhase
from src.Utils.Settings.PhaseConfig import PhaseConfig
from src.Core.Entities.Mine import Mine
from src.Utils.Enums.Orientation import Orientation


class ExtendedPlacementPhase(PlacementPhase):
    def __init__(self, config: PhaseConfig):
        """
        Initialize the ExtendedPlacementPhase with configuration.
        
        This phase extends the basic placement phase by adding mines to the game objects.
        
        Args:
            config: PhaseConfig object containing all initialization parameters
        """
        super().__init__(config)

    def create_game_objects(self, orientation):
        base = super().create_game_objects(Orientation.HORIZONTAL)
        base.extend([Mine(), Mine(), Mine()])
        return base