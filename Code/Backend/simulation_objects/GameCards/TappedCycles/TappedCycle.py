from ..Land import Land

class TappedCycle(Land):
    def __init__(self, card, mandatory=False, **kwargs):
        Land.__init__(self, card, mandatory, **kwargs)
        self._permatap = True
