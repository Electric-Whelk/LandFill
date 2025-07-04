from simulation_objects.CardCollections.Deck import Deck

class Simulation:
    def __init__(self, deck):
        self._deck = deck

    #setters and getters
    @property
    def deck(self) -> Deck:
        return self._deck
