import itertools
from itertools import product, combinations


from .CardCollection import CardCollection
from simulation_objects.GameCards import Land
from simulation_objects.Misc.Wodge import Wodge
from ..GameCards.FilterLands.RampLand import RampLand

class Battlefield(CardCollection):
    def __init__(self):
        CardCollection.__init__(self)
        self._permutations = []
        self._perms_as_dicts = []
        #print(f"Set permutations as: {self._permutations}")

    #getters and setters
    @property
    def permutations(self) -> list:
        return self._permutations
    @permutations.setter
    def permutations(self, value):
        self._permutations = value

    @property
    def perms_as_dicts(self) -> list:
        return self._perms_as_dicts
    @perms_as_dicts.setter
    def perms_as_dicts(self, value):
        self._perms_as_dicts = value

    #pseudogetters
    def accessible_mana(self) -> list[Land]:
        return [l for l in self.card_list if not l.tapped and isinstance(l, Land)]

    def max_mana(self) -> int:
        return len(self.accessible_mana())

    def filters(self) -> list:
        return [x for x in self.card_list if isinstance(x, RampLand)]

    #game actions
    def untap(self):
        for card in self._cards:
            card.tapped = False


    #game information
    def handle_costed(self, combos):
        #as programmed this returns nothing, it only messes about in the lac
        pass


    def reset_permutations(self, game, extra_land=None):
        #all_info = [{"land": x, "produced":x.conditions(game)} for x in self.accessible_mana()]
        mana = self.accessible_mana()
        if extra_land != None and extra_land.enters_untapped(game):
            mana.append(extra_land)
        all_produced = [x.conditions(game) for x in mana]
        all_combinations = product(*all_produced)
        lac = list(all_combinations)
        if len(self.filters()) > 0:
            self.handle_costed(lac)
        self.permutations = lac
        #self.perms_as_dicts = self.perms_to_dicts(lac)
        #print(f"Created {len(self.permutations)} permutations out of {mana}")




        #return list(all_combinations)




    def encode_lump(self, game, lump):

        """
        if n is None:
            accessible = [(self.accessible_mana())]
        else:
            accessible = list(itertools.combinations(self.accessible_mana(), n))

            """

        lands = self.accessible_mana()

        accessible = list(itertools.combinations(lands, len(lands)))


        for bunch in accessible:
            #assert(len(bunch) == lump.cmc)
            lump.parse_wodge(Wodge(bunch, game))

        """
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

        """

    def perms_to_dicts(self, input:list):
        output = []
        for option in input:
            colors = [x['color'] for x in option]
            dict = {'W':0, 'U':0, 'B':0, 'R':0, 'G':0, 'C':0}
            for color in colors:
                dict[color] += 1
            output.append(dict)
        return output










