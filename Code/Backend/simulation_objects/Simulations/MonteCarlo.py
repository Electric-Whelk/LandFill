#from simulation_objects.CardCollections.player_deck import player_deck
import functools
import pickle
from copy import deepcopy

import numpy
from joblib import delayed, Parallel
from matplotlib import pyplot as plt
from scipy.stats import skew, kurtosis
from statsmodels.distributions.empirical_distribution import ECDF

from simulation_objects.CardCollections.DelayedFunctions import run_tests_exterior
from simulation_objects.GameCards import BasicLand, Land
from simulation_objects.Misc.ColorPie import landtype_map
from simulation_objects.Simulations.Game import Game
from simulation_objects.Simulations.Simulation import Simulation
from datetime import datetime
import time
import pandas as pd
from simulation_objects.Timer import functimer_once


class MonteCarlo(Simulation):
    def __init__(self, deck, turns=10, runs=None, ct_runs=100, close_examine=False, timer=False):
        Simulation.__init__(self, deck)
        self._wasteless_turns = 0
        self._wasteless_games = 0
        self._wasted_mana = []
        self._turns = turns
        self._lands = self.deck.lands_list()
        self._ct_runs = ct_runs

        #stats attributes used in analysis
        self._turn_proportions = 0
        self._game_proportions = 0
        self._worst_performing_card = None

        #dev attributes
        self.like_for_like = False
        self._close_examine = close_examine
        self._timer = timer
        if self._close_examine:
            self._runs = 1
        else:
            self._runs = 1000 #CHANGE BACK TO ONE THOUSAND (and ct is 300)
        if runs != None:
            self._runs = runs

        #Initial: 1000 runs, 300 ct runs
        #Small test: 500 runs, 100 ct runs
        #NormalTest: 1000 runs, 200 ct runs
        #Doubletest: 2000 runs, 400 ct runs
        #BigTest: 10000 runs, 2000 ct runs.
        #UnevenTest: 300 runs, 1000 ct_runs
        #TinyTest: 100, 50
        #TinyRebalance: 100, 100

        #variables returned by the test
        self._runtime = 0

    @property
    def wasted_mana(self):
        return self._wasted_mana
    @wasted_mana.setter
    def wasted_mana(self, value):
        self._wasted_mana = value

    @property
    def worst_performing_card(self) -> Land:
        return self._worst_performing_card
    @worst_performing_card.setter
    def worst_performing_card(self, card:Land):
        self._worst_performing_card = card

    @property
    def game_proportions(self) -> float:
        return self._game_proportions
    @game_proportions.setter
    def game_proportions(self, value):
        self._game_proportions = value

    @property
    def ct_runs(self) -> int:
        return self._ct_runs

    @property
    def wasteless_games(self) -> int:
        return self._wasteless_games
    @wasteless_games.setter
    def wasteless_games(self, value):
        self._wasteless_games = value



    @property
    def turn_proportions(self) -> float:
        return self._turn_proportions
    @turn_proportions.setter
    def turn_proportions(self, value):
        self._turn_proportions = value

    @property
    def turns(self):
        return self._turns

    @property
    def lands(self):
        return self._lands

    @property
    def wasteless_turns(self) -> int:
        return self._wasteless_turns
    @wasteless_turns.setter
    def wasteless_turns(self, value: int):
        self._wasteless_turns = value


    @property
    def runs(self):
        return self._runs

    #run!
    def run_v1(self):
        #print("Running tests!")
        starttime = time.time()


        mana_per_game_array = []
        on_curve_spend = []
        leftover = []
        wasteless_games = 0
        for i in range(0, self._runs):#SCAFFOLD - currently at 6 seconds per 10,000 games
            if self._timer and i % 1000 == 0:
                print(f"{i}...")
            g = Game(self.deck, turns=self.turns, verbose=self._close_examine)
            g.run()


            #options_per_turn += (g.options_per_turn/self.runs)
            mana_per_game_array.append(g.total_spent_mana)
            on_curve_spend.append(g.castable_cmc_in_hand)
            leftover.append(g.leftover_mana)
            if g.leftover_mana == 0:
                wasteless_games += 1
                self.get_game_info(g)


        all_lands = self.deck.lands_list()
        for land in all_lands:
            land.to_mean()
        ranked = sorted(all_lands, key=lambda x: x.proportion_of_turns(), reverse=True)
        endtime = time.time()
        diff = endtime - starttime


        #nonbasics = [l for l in self.deck.lands_list() if not isinstance(l, BasicLand)]
        #assert len(nonbasics) == 1
        #print(f"{nonbasics[0].grade['Mana']}")

        #print(f"average spend -> mean: {numpy.mean(mana_per_game_array)} med: {numpy.median(mana_per_game_array)} std: {numpy.std(mana_per_game_array)} skew: {skew(mana_per_game_array)}")
        print(f"Leftover spend -> mean {numpy.mean(leftover)} std: {numpy.std(leftover)} med: {numpy.median(leftover)} skew: {skew(leftover)} kurtosis: {kurtosis(leftover)}")
        #print(f"{kurtosis(leftover)}")
        print(f"In {self.wasteless_turns} out of {self.runs} ({self.wasteless_turns/70000}), you wasted no mana")

        #print(f"\nShockproblems: {shock} Painproblems: {pain} Fetchproblems: {fetch}")




        print(f"Finished ({diff})")

        i = 1

        for land in ranked:
            #print(f"{i}: {land} appeared {land.grade["Appearances"]} times, allowing for the spending of {land.grade["Mana"]} mana and {land.grade["Options"]} options")
            print(f"{i}: {land.name} appeared {land.turn_appearances}  times, allowing zero waste {land.proportion_of_turns()} times, proportionally, wasting on average {land.average_wasted()}")
            land.reset_grade()
            i += 1

    #@functimer_once
    def run_deck_test(self):
        dev_values = ["proportion_of_turns", "proportion_of_games"]
        dev_value = dev_values[1]

        self.reset_lands()
        self.run_tests()

        self.assess_deck()
        #self.assess_lands()
        ranked = self.rank_lands(dev_value)
        #self.weighted_average([x for x in ranked if isinstance(x, BasicLand)])

        #self.print_deck_details(dev_value)
        #self.print_list(ranked, dev_value)

    def run(self):
        self.deck.reset_card_score()
        self.run_tests()
        self.assess_deck_hc()
        self.assess_lands_hc()


    def individual_deck_test(self):
        self.deck.reset_card_score()
        self.run_tests(quit=False)
        self.assess_deck_hc()
        self.assess_lands_hc()

    def assess_deck_hc(self):
        self.game_proportions = self.wasteless_games / self.runs


    def assess_lands_hc(self):
        for card in self.deck.lands_list():
            p = card.proportion_of_games()

        worst = None
        worst_score = 0

        after_sorting = sorted(self.deck.lands_list(), key=lambda x: x.proportions, reverse=False)
        print("Running test")

        for i in range(len(self.deck.lands_list())):
            rank = len(self.deck.lands_list()) - i
            print(f"\t {rank}: {after_sorting[i]} -> {after_sorting[i].proportions} -> {numpy.median(after_sorting[i].options)}")

        candidates = self.get_worst_card_candidates(self.deck.card_list)
        for card in candidates:

            if isinstance(card, Land):
                if card.mandatory == True:
                    #card.reset_grade()
                    x=3
                else:
                    if worst == None or card.proportions < worst_score:
                        worst = card
                        worst_score = card.proportions
                    #card.reset_grade()

        self.worst_performing_card = worst

    def get_worst_card_candidates(self, card_list):
        output = []
        for card in card_list:
            if card.mandatory == False:
                if not any(item in card.inferior_lands for item in card_list):
                    output.append(card)
        return output




    def normalize_basics(self, basicname):
        basicscores = [x.proportion_of_games() for x in self.deck.card_list if x.name == basicname]
        #print(f"{basicname} scores: {basicscores}")
        med = numpy.median(basicscores)
        for card in self.deck.card_list:
            if card.name == basicname:
                card.proportions = med


    def single_card_test(self, card_in):
        g = Game(self.deck, turns=self.turns)
        g.run(card_to_test=card_in)
        return self.wastelessness(g)





    def print_deck_details(self, criterion):
        match criterion:
            case "proportion_of_turns":
                print(f"{self.turn_proportions} <- {self.wasteless_turns} wasteless turns out of {self.total_turns()} ")
            case "proportion_of_games":
                print(f"{self.game_proportions} <- {self.wasteless_games} wasteless games out of {self.runs} ")

    def total_turns(self):
        return self.turns * self.runs

    def assess_deck(self):
        self.turn_proportions = self.wasteless_turns / self.total_turns()
        self.game_proportions = self.wasteless_games / self.runs

    def assess_lands(self):
        for land in self.lands:
            land.above_average_wasteless_turns = land.proportion_of_turns() >= self.turn_proportions
            land.above_average_wasteless_games = land.proportion_of_games() >= self.game_proportions


    def print_list(self, input, criterion=None):
        i = 1
        for item in input:
            match criterion:
                case "proportion_of_turns":
                    print(f"{i}: {item} -> {item.proportion_of_turns()} over {item.turn_appearances} appearances {self.format_rank_position(item.above_average_wasteless_turns)}")
                case "proportion_of_games":
                    print(f"{i}: {item} -> {item.proportion_of_games()} over {item.appearances()} appearances {self.format_rank_position(item.above_average_wasteless_games)}")
                case _:
                    print(f"{i}: {item} -> {item.proportions}")
                    #raise Exception(f"{criterion} is not a valid criterion for print_list")
            i += 1

    def format_rank_position(self, test):
        if test:
            return "ABOVE"
        else:
            return "BELOW"



    def rank_lands(self, criterion):
        match criterion:
            case "proportion_of_turns":
                return sorted(self.lands, key=lambda x: x.proportion_of_turns(), reverse=True)
            case "proportion_of_games":
                return sorted(self.lands, key=lambda x: x.proportion_of_games(), reverse=True)
            case _:
                raise Exception(f"{criterion} is not a valid input to test.rank_lands()")


    def reset_lands(self):
        for land in self.lands:
            land.reset_grade()



    def run_tests(self, quit=True):
        for i in range(0, self._runs):
            g = Game(self.deck, turns=self.turns, verbose=self._close_examine)
            g.run(quit=quit)
            self.get_game_info(g)



    def get_game_info(self, game):
        self.wasteless_turns += game.wasteless_turns
        self.wasteless_games += self.wastelessness(game)
        self.wasted_mana.append(game.leftover_mana)

    def wastelessness(self, game) -> int:
        if game.leftover_mana == 0:
            return 1
        return 0

    def most_represented_basics(self, input:list[Land]):
        above_dict = {}
        below_dict = {}
        for item in input:
            if isinstance(item, BasicLand):
                if item.above_average_wasteless_games:
                    self.add_or_increase_dict(above_dict, item.name)
                else:
                    self.add_or_increase_dict(below_dict, item.name)
        print(f"Abovedict: {above_dict} Belowdict: {below_dict}")

    def add_or_increase_dict(self, dict, item):
        if item not in dict:
            dict[item] = 1
        else:
            dict[item] += 1

    def format_pandas_dataframe(self, input):
        i = 1
        data = []
        for item in input:
            data.append({
                'rank': i,
                'name': item.name,
                'score': item.proportion_of_games(),
                'appearances': item.appearances(),
            })
            i += 1
        return pd.DataFrame(data)

    def weighted_average(self, ranked_list):
        df = self.format_pandas_dataframe(ranked_list)

        # Group by individual land name and compute weighted average rank
        war_by_land = df.groupby('name')[['rank', 'appearances']].apply(
            lambda g: (g['rank'] * g['appearances']).sum() / g['appearances'].sum()
        ).sort_values()

        print("Weighted Average Rank by Land:")
        print(war_by_land)


    #def worst_performing_card(self):
        #return min(self.lands, key=lambda x: x.proportion_of_games())

    def determine_cumulative_distribution(self):

        #numpy.sort(self.wasted_mana)
        #c = numpy.arange(1, len(self.wasted_mana) + 1) / len(self.wasted_mana)
        e = ECDF(self.wasted_mana)
        #area = numpy.trapz(x=e.x, y=e.y)


        x = list(e.x[1:])
        y = list(e.y[1:])
        x.append(30)
        y.append(1)

        print("x:", x)
        print("y:", y)
        plt.step(x, y, color='green')
        plt.xlabel('Data Values')
        plt.ylabel('CDF')
        plt.title('CDF via ECDF')
        plt.grid()
        plt.show()


        from scipy.integrate import trapezoid

        area = trapezoid(x=x, y=y)

        #values, counts = numpy.unique(self.wasted_mana, return_counts=True)
        #cum_counts = numpy.cumsum(counts)
        #area = numpy.trapz(cum_counts, x=values)
        return area