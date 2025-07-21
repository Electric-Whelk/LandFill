from operator import truediv
from simulation_objects.GameCards.SearchLands import SearchLand
from simulation_objects.GameCards.SearchLands import FetchLand


class Moot:
    def __init__(self, option, colors, generic):
        self._option = option
        self._pips = colors
        self._generic = generic
        self._castable = generic == 0 and len(colors) == 0
        self._pure_generic = len(colors) == 0 and not self._castable
        self._includes_searchland = self.check_for_searchland(option)


    #getters and setters
    @property
    def includes_searchland(self) -> bool:
        return self._includes_searchland

    @property
    def castable(self):
        return self._castable

    @property
    def pips(self):
        return self._pips

    @property
    def pure_generic(self):
        return self._pure_generic

    @property
    def generic(self):
        return self._generic

    @property
    def option(self):
        return self._option

    def accept_mana_submission(self, sub, game):
        totalneeded = len(self.pips) + self.generic
        quant = sub.increase(game)
        available = quant + game.battlefield.max_mana()
        #print(f"\t\tneeds {totalneeded}, has {available}")
        return quant >= totalneeded


    def check_for_searchland(self, option):
        if option is None:
            return False
        for op in option:
            land = op["land"]
            if isinstance(land, SearchLand):
                return True
        return False



    def accept_submission(self, sub) -> bool:
        if self.pure_generic:
            if self.generic <= len(sub):
                return True
            return False
        #if sub in self._pips:
        for color in sub:
            if color in self._pips:
                return True
        return False

    def tap_moot_mana(self, game):
        for entity in self.option:
            entity['land'].tap_for(game, entity['color'])


    def searchland_agnostic(self, lump) -> bool:
        if self.castable == False:
            return False
        #WILL NOT WORK, just pausing here while I try another approach
        return True

    def generalize_searchland(self, lump):
        divided = self.seperate_searchland(self.option)
        if len(lump.check_pip_castability(divided["others"])) == 0:
            divided["search"]["color"] = "Any"


    def seperate_searchland(self, input):
        oth = []
        sea = []
        for item in input:
            if isinstance(item["land"], SearchLand):
                sea.append(item)
            else:
                oth.append(item)
        l = len(sea)
        if l == 1:
            return {
                "others": oth,
                "search": sea[0]
            }
        elif l <= 0:
            raise Exception("Seperate Searchland called on a moot without a search")
        else:
            raise Exception("Ended up with multiple searchlands in a moot!")





