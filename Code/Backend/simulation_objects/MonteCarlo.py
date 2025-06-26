from simulation_objects.Deck import Deck

class MonteCarlo:
    def __init__(self, deck):
        self._deck = deck


    @property
    def deck(self) -> Deck:
        return self._deck


    def test_reference(self, int):
        self.deck.test_int = int





