from simulation_objects.GameCards.Land import Land

class BasicLand(Land):
    def __init__(self, card, zone, **kwargs):
        Land.__init__(self, card, zone, **kwargs)
        self._monocolor = True

