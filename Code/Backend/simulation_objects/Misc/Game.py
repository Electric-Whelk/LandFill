

from simulation_objects.CardCollectiions.Battlefield import Battlefield
from simulation_objects.CardCollectiions.CardCollection import CardCollection
from simulation_objects.CardCollectiions.Deck import Deck
from simulation_objects.CardCollectiions.Graveyard import Graveyard
from simulation_objects.CardCollectiions.Hand import Hand
from simulation_objects.Misc.Simulation import Simulation


class Game(Simulation):
    def __init__(self, deck):
        Simulation.__init__(self, deck)
        self._hand = Hand()
        self._battlefield = Battlefield()
        self._graveyard = Graveyard()

    #getters
    @property
    def hand(self) -> Hand:
        return self._hand

    @property
    def battlefield(self) -> Battlefield:
        return self._battlefield

    @property
    def graveyard(self) -> Graveyard:
        return self._graveyard

    #run!
    def run(self):
        self.setup_game()
        for _ in range(10): #SCAFFOLD - number of turns
            self.run_turn()
        pass

    def run_turn(self):
        self.battlefield.untap()
        self.draw()
        self.determine_play()

    def setup_game(self):
        self.deck.shuffle()
        self.draw(7)


    #game actions
    def draw(self, repeats=1):
        for _ in range(repeats):
            self.deck.give_top(self.hand)


    #strategizing algorithms
    def determine_play(self):
        on_field = self.battlefield.determine_available_mana()




