from simulation_objects.GameCards import BasicLand
from simulation_objects.GameCards.UntappableCycles.UntappableLand import UntappableLand

class BattleLand(UntappableLand):

    def enters_untapped(self, game) -> bool:
        return sum(1 for x in game.battlefield.lands_list() if isinstance(x, BasicLand)) >= 1

