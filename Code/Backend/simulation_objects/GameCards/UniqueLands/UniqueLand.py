from simulation_objects.GameCards.Land import Land

class UniqueLand(Land):
    def __init__(self, card, mandatory=False, **kwargs):
        Land.__init__(self, card, mandatory=mandatory, **kwargs)
        self._cycle = card._name
        self._cycle_display_name = card.name

