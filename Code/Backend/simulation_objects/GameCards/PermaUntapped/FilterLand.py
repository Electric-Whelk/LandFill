from simulation_objects.GameCards.PermaUntapped import PermaUntapped
from simulation_objects.GameCards.SubLand import SubLand


class FilterLand(PermaUntapped):
    def __init__(self, card, mandatory=False, **kwargs):
        PermaUntapped.__init__(self, card, mandatory=mandatory, **kwargs)
        subland_produced = self.set_subland_produces(self._produced)
        names = self.get_subland_names()
        self._required = self.set_required(subland_produced)
        self._sublands = [SubLand(card, produced=subland_produced, name=names[0]),
                          SubLand(card, produced=subland_produced, name=names[1])]


    @property
    def sublands(self):
        for subland in self._sublands:
            subland.tapped = False
        return self._sublands

    @property
    def required(self):
        return self._required


    def get_subland_names(self):
        return [f'1_{self}', f"2_{self}"]

    def set_required(self, input):
        return input


    def set_subland_produces(self, produced):
        output = []
        for color in produced:
            if color != "C":
                output.append(color)
        return output

    def heap_prod(self, deck):
        if deck.colorless_pips:
            return self.produced
        else:
            return [color for color in self.produced if color != "C"]

    def live_prod(self, game, filterblacklist=None):
        if filterblacklist is None:
            filterblacklist = []
        filterblacklist = filterblacklist + [self]
        all_lands = game.battlefield.lands_list(exclude=filterblacklist)
        filterlands = []
        for land in all_lands:
            if isinstance(land, FilterLand):
                filterlands.append(land)
            else:
                if land.produces_at_least_one(self.required, game):
                    return self.produced

        for card in filterlands:
            if card.produces_at_least_one(self.required, game, filterblacklist=filterblacklist):
                return self.produced

        return ["C"]

        """try:
            for card in nonfilters:
                if isinstance(card, FilterLand):
                    if card.produces_at_least_one(self.required, game, filterblacklist=filterblacklist):
                        return self.produced
                elif card != self and card.produces_at_least_one(self.required, game):
                    return self.produced

            return ["C"]

        except RecursionError:
            raise Exception(f"Recursion error on battlefield {game.battlefield.card_list}")"""

    def produces_at_least_one(self, inputlist, game, live=True, filterblacklist=[]):
        if live:
            prod = self.live_prod(game, filterblacklist=filterblacklist)
        else:
            prod = self.produced
        return bool(set(prod) & set(inputlist))





    """def live_prod_contribution_subtraction(self, game):
        for land in game.battlefield.lands_list():
            if not isinstance(land, FilterLand):
                if land.produces_at_least_one(self.required, game):
                    return self.required
            else:
                if land.live_prod_contribution_subtraction(game):
                    if land.produces_at_least_one(self.required, game, filter_override=True):
                        return self.required
        return ["C"]"""

    """def produces_at_least_one(self, inputlist, game, filter_override=False):
        if filter_override:
            prod = self.required
        else:
            prod = self.live_prod(game)
        for color in prod:
            if color in inputlist:
                return True
        return False"""

    def set_price(self, game, color):
        if color == "None":
            return self.generic_price
        if not self.tapped:
            if color == "Gen":
                return self.generic_price
        return 9999

