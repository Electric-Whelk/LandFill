from simulation_objects.GameCards.Land import Land

class BasicLand(Land):
    def __init__(self, card, zone):
        Land.__init__(self, card, zone)
        self._monocolor = True

