#from simulation_objects.CardCollections.Deck import Deck
import numpy
from scipy.stats import skew, kurtosis

from simulation_objects.GameCards import BasicLand
from simulation_objects.Simulations.Game import Game
from simulation_objects.Simulations.Simulation import Simulation
from datetime import datetime
import time

class Test(Simulation):
    def __init__(self, deck, cache, close_examine=False, timer=False):
        Simulation.__init__(self, deck)
        self._cache = cache

        #dev attributes
        self._close_examine = close_examine
        self._timer = timer
        if self._close_examine:
            self._runs = 1
        else:
            self._runs = 10000 #CHANGE BACK TO TEN THOUSAND

        #variables returned by the test
        self._runtime = 0

    @property
    def cache(self):
        return self._cache

    @property
    def runs(self):
        return self._runs

    #run!
    def run(self):
        #print("Running tests!")
        starttime = time.time()


        mana_per_game_array = []
        on_curve_spend = []
        leftover = []
        wasteless_games = 0
        for i in range(0, self._runs):#SCAFFOLD - currently at 6 seconds per 10,000 games
            if self._timer and i % 1000 == 0:
                print(f"{i}...")
            g = Game(self.deck, self.cache, verbose=self._close_examine)
            g.run()

            #options_per_turn += (g.options_per_turn/self.runs)
            mana_per_game_array.append(g.total_spent_mana)
            on_curve_spend.append(g.castable_cmc_in_hand)
            leftover.append(g.leftover_mana)
            if g.leftover_mana == 0:
                wasteless_games += 1


        all_lands = self.deck.lands_list()
        for land in all_lands:
            land.to_mean()
        ranked = sorted(all_lands, key=lambda x: x.proportion(), reverse=True)
        endtime = time.time()
        diff = endtime - starttime


        #nonbasics = [l for l in self.deck.lands_list() if not isinstance(l, BasicLand)]
        #assert len(nonbasics) == 1
        #print(f"{nonbasics[0].grade['Mana']}")

        #print(f"average spend -> mean: {numpy.mean(mana_per_game_array)} med: {numpy.median(mana_per_game_array)} std: {numpy.std(mana_per_game_array)} skew: {skew(mana_per_game_array)}")
        print(f"Leftover spend -> mean {numpy.mean(leftover)} std: {numpy.std(leftover)} med: {numpy.median(leftover)} skew: {skew(leftover)} kurtosis: {kurtosis(leftover)}")
        #print(f"{kurtosis(leftover)}")
        print(f"In {wasteless_games} out of {self.runs} ({wasteless_games/10000}), you wasted no mana")

        #print(f"\nShockproblems: {shock} Painproblems: {pain} Fetchproblems: {fetch}")




        print(f"Finished ({diff})")

        i = 1

        for land in ranked:
            #print(f"{i}: {land} appeared {land.grade["Appearances"]} times, allowing for the spending of {land.grade["Mana"]} mana and {land.grade["Options"]} options")
            print(f"{i}: {land.name} appeared {land.appearances()}  times, allowing zero waste {land.proportion()} times, proportionally, wasting on average {land.average_wasted()}")
            land.reset_grade()
            i += 1