from operator import truediv


class Moot:
    def __init__(self, option, colors, generic):
        self._option = option
        self._pips = colors
        self._generic = generic
        self._castable = generic == 0 and len(colors) == 0
        self._pure_generic = len(colors) == 0 and not self._castable


    #getters and setters
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
        x = 4
        for entity in self.option:
            entity['land'].tap_for(game, entity['color'])


