#from simulation_objects.CardCollections.Deck import Deck
from simulation_objects.Simulations.Game import Game
from simulation_objects.Simulations.Simulation import Simulation
from datetime import datetime
import time

class Test(Simulation):
    def __init__(self, deck, close_examine=False, timer=False):
        Simulation.__init__(self, deck)

        #dev attributes
        self._close_examine = close_examine
        self._timer = timer
        if self._close_examine:
            self._runs = 1
        else:
            self._runs = 10000 #CHANGE BACK TO TEN THOUSAND

    @property
    def runs(self):
        return self._runs

    #run!
    def run(self):
        print("Running tests!")
        starttime = time.time()

        decisions = 0
        mana_per_game = 0
        options_per_turn = 0
        for i in range(0, self._runs):#SCAFFOLD - currently at 6 seconds per 10,000 games
            if self._timer and i % 100 == 0:
                print(f"{i}...")
            g = Game(self.deck, verbose=self._close_examine)
            g.run()
            decisions += g.decisions
            mana_per_game += (g.total_spent_mana/self.runs)
            options_per_turn += (g.options_per_turn/self.runs)
        print(f"Made a total of {decisions} decisions, spending an average of {mana_per_game} mana and having around {options_per_turn} choices each turn")
        all_lands = self.deck.lands_list()
        ranked = sorted(all_lands, key=lambda x: int(x.grade["Mana"] * 1000), reverse=True)
        endtime = time.time()
        diff = endtime - starttime
        print(f"Finished ({diff})")
        for land in ranked:
            land.to_mean(self.runs)
            print(f"{land} appeared {land.grade["Appearances"]} times, allowing for the spending of {land.grade["Mana"]} mana and {land.grade["Options"]} options")
            land.reset_grade()