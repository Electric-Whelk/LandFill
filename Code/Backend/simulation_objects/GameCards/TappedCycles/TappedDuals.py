from .TappedCycle import TappedCycle

class TappedDuals(TappedCycle):
    def __init__(self, card, mandatory=False):
        TappedCycle.__init__(self, card, mandatory)
        self._typed = True