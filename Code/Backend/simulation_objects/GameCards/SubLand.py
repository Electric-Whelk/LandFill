from simulation_objects.GameCards import Land


class SubLand(Land):
    def __init__(self, card, produced=[], name=None):
        Land.__init__(self, card)
        if produced != []:
            self._produced = produced
        if name is not None:
            self._name = name