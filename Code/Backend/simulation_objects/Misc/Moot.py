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


