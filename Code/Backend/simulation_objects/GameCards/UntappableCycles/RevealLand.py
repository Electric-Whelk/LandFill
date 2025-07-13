from .UntappableLand import UntappableLand
from simulation_objects.Misc.ColorPie import landtype_map

class RevealLand(UntappableLand):

    def enters_untapped(self, game) -> bool:
        untap_criteria = [landtype_map[initial] for initial in self.produced]
        for land in game.hand.lands_list():
            types = land.landtypes
            for criterion in untap_criteria:
                if criterion in types:
                    return True
        return False