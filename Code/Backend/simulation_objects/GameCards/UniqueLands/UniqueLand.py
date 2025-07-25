from simulation_objects.GameCards.Land import Land

class UniqueLand(Land):
    def __init__(self, card, mandatory=False):
        Land.__init__(self, card, mandatory=mandatory)
        self._cycle = card._name

