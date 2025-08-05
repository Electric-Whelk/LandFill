from .TappedCycle import TappedCycle


class Triome(TappedCycle):
    def __init__(self, card, mandatory=False, **kwargs):
        TappedCycle.__init__(self, card, mandatory)
        self.peek = False
