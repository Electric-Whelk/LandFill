from simulation_objects.GameCards.PermaUntapped import PermaUntapped
from simulation_objects.GameCards.UntappableCycles.SubLand import SubLand


class FilterLand(PermaUntapped):
    def __init__(self, card, mandatory=False):
        PermaUntapped.__init__(self, card, mandatory=mandatory)
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

    def live_prod(self, game, filterblacklist=[]):
        filterblacklist.append(self)
        otherfilters = []
        all_lands = game.battlefield.lands_list(exclude=filterblacklist)
        try:
            for card in all_lands:
                if isinstance(card, FilterLand):
                    if card.produces_at_least_one(self.required, game, filterblacklist=filterblacklist):
                        return self.produced
                elif card != self and card.produces_at_least_one(self.required, game):
                    return self.produced

            """for filter in otherfilters:
                if filter.produces_at_least_one(self.required, game, live=False):
                    for card in game.battlefield.lands_list():"""
            return ["C"]


        except RecursionError:
            raise Exception(f"Recursion error on battlefield {game.battlefield.card_list}")

    def produces_at_least_one(self, inputlist, game, live=True, filterblacklist=[]):
        if live:
            prod = self.live_prod(game, filterblacklist=filterblacklist)
        else:
            prod = self.produced
        for color in prod:
            if color in inputlist:
                return True
        return False




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

