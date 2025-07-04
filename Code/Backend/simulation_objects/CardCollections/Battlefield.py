from itertools import product

import simulation_objects.CardCollections as CC
import simulation_objects.GameCards as GC

class Battlefield(CC.CardCollection):

    #pseudosetters
    def accessible_mana(self) -> list[GC.Land]:
        return [l for l in self.card_list if not l.tapped]

    #game actions
    def untap(self):
        for card in self._cards:
            card.tapped = False


    #game information
    def mana_combinations(self, game):
        landinfo = []
        for land in self.accessible_mana():
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
        return output









