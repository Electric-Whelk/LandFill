import itertools
from itertools import product, combinations


from .CardCollection import CardCollection
from simulation_objects.GameCards import Land
from simulation_objects.Misc.Wodge import Wodge

class Battlefield(CardCollection):

    #pseudogetters
    def accessible_mana(self) -> list[Land]:
        return [l for l in self.card_list if not l.tapped]

    def max_mana(self) -> int:
        return len(self.accessible_mana())

    #game actions
    def untap(self):
        for card in self._cards:
            card.tapped = False


    #game information
    def mana_combinations(self, game, lump):

        """
        if n is None:
            accessible = [(self.accessible_mana())]
        else:
            accessible = list(itertools.combinations(self.accessible_mana(), n))

            """

        accessible = list(itertools.combinations(self.accessible_mana(), lump.cmc))

        for bunch in accessible:
            assert(len(bunch) == lump.cmc)
            lump.parse_wodge(Wodge(bunch, game))






        metaout = []
        for arrangement in accessible:
            landinfo = []
            for land in arrangement:
                d = {
                    "land":land,
                    "produced": land.conditions(game)
                }
                landinfo.append(d)
                grouped = [land["produced"] for land in landinfo]
            combinations = product(*grouped)
            output = []

            for c in combinations:
                colours = [x["color"] for x in c]
                output.append(c)
            metaout.append(output)
        return metaout









