from simulation_objects.GameCards.Land import Land

class SearchLand(Land):
    def __init__(self, card, basic_only, mandatory=False):
        Land.__init__(self, card, mandatory)
        self._basic_only = basic_only
        self._searchable = card.check_searched_lands_comprehensive()
        #print(f"{self.name}:{self.searchable}")

    @property
    def basic_only(self):
        return self._basic_only

    @property
    def searchable(self):
        return self._searchable

