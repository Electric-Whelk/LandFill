#from simulation_objects.CardCollections.Deck import Deck
from simulation_objects.Simulations.Game import Game
from simulation_objects.Simulations.Simulation import Simulation
from datetime import datetime

class Test(Simulation):
    def __init__(self, deck, close_examine=False, timer=False):
        Simulation.__init__(self, deck)

        #dev attributes
        self._close_examine = close_examine
        self._timer = timer
        if self._close_examine:
            self._runs = 1
        else:
            self._runs = 10000

    #run!
    def run(self):
        decisions = 0
        mana_per_game = 0
        options_per_turn = 0
        for i in range(0, self._runs):#SCAFFOLD - currently at 6 seconds per 10,000 games
            if self._timer and i % 100 == 0:
                print(f"{i}...")
            g = Game(self.deck, verbose=self._close_examine)
            g.run()
            decisions += g.decisions
            mana_per_game += (g.total_spent_mana/10000)
            options_per_turn += (g.options_per_turn/10000)
        print(f"Made a total of {decisions} decisions, spending an average of {mana_per_game} mana and having around {options_per_turn} choices each turn")