from simulation_objects.CardCollectiions.Deck import Deck

class Simulation:
    def __init__(self, deck):
        self._deck = deck

    #setters and getters
    def deck(self) -> Deck:
        return self._deck
