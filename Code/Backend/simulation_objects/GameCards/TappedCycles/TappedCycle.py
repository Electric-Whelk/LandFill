from ..Land import Land

class TappedCycle(Land):
    def __init__(self, card, mandatory=False):
        Land.__init__(self, card, mandatory)
        self.permatap = True
