import time
import random
from copy import deepcopy

import numpy
import numpy as np
from currency_converter import CurrencyConverter
from line_profiler import profile
from numpy import median
from numpy.ma.core import set_fill_value
from scipy.signal import savgol_filter
from sqlalchemy import false

from database_management.models.Card import Card
from Extensions import db
from math import inf, ceil

from simulation_objects.CardCollections.CardCollection import CardCollection
from simulation_objects.CardCollections.Deck import Deck
from simulation_objects.GameCards import FastLand, ShockLand, MiscLand, BondLand, CheckLand, SlowLand, RevealLand, \
    PainLand, HorizonLand
from simulation_objects.GameCards.BasicLand import BasicLand
from simulation_objects.GameCards.GameCard import GameCard
from simulation_objects.GameCards.Land import Land
from simulation_objects.GameCards.PermaUntapped import FilterLand, Verge
from simulation_objects.GameCards.SearchLands.FetchLand import FetchLand
from simulation_objects.GameCards.TappedCycles.GuildGate import GuildGate
from simulation_objects.GameCards.TappedCycles.Triome import Triome
from simulation_objects.Misc.ColorPie import colortype_map, landtype_map
from simulation_objects.Misc.LandPrioritization import stdprioritization, LandPrioritization
from simulation_objects.Simulations.Test import Test
from simulation_objects.Misc.LandPermutationCache import LandPermutationCache
from simulation_objects.Timer import functimer_perturn, functimer_once


class MonteCarlo(CardCollection):
    def __init__(self, deck, close_examine=False, timer=False, verbose=False):
        CardCollection.__init__(self)
        #set on creation of the object
        self._deck = deck
        self._prioritization = stdprioritization
        self._prioritization_object = LandPrioritization(stdprioritization)
        self._sample_pound = CurrencyConverter().convert(1, "GBP", "USD")


        #set when the deck is setup
        self._colorless_pips = None
        self._pie_slices = None
        self._categories = None
        self._minbasics = 0
        
        self.halt = False

        #will figure out when to set the below
        """
        self._prioritization= {
            "Command Tower": 1,
            "Filter Lands": 1,
            "Triomes": 1,
            "Shock Lands": 1,
            "Basic Lands": 1,
            "OG Dual Lands": 1,
            "Fetch Lands": 1,
            "Tri-Color Taplands": 2,
            "Bond Lands": 2,
            "Verge Lands": 2,
            "Pain Lands": 2,
            "Horizon Lands": 2,
            "Check Lands": 3,
            "Reveal Lands": 3,
            "Battle Lands": 2,
            "Fast Lands": 3,
            "Slow Lands": 3,
            "Guildgates": 4
        }"""


        #requirements - set at the start of each run
        self._budget = float(inf)
        self._mppc = None #max price per card
        self._currency = "GBP" #is there a more elegant way to set default?
        self._threshold = float(inf)
        self._minbasics = 0

        #session variables - globally stored variables used during the run
        self._permitted_lands = []
        self._remaining = 0
        self._optimized = []

        #dev variables
        self._close_examine = close_examine
        self._timer = timer
        self._verbose = verbose
        self.swapped_out_nonbasics = []



    #setters and getters
    @property
    def sample_pound(self):
        return self._sample_pound

    @property
    def stdprioritization(self):
        return self._prioritization

    @property
    def prioritization_object(self):
        return self._prioritization_object

    @property
    def minbasics(self):
        return self._minbasics
    @minbasics.setter
    def minbasics(self, value):
        self._minbasics = value

    @property
    def prioritization(self):
        return self._prioritization

    @property
    def categories(self):
        return self._categories

    @property
    def pie_slices(self):
        return self._pie_slices

    @property
    def colorless_pips(self):
        return self._colorless_pips

    #@property
    #def cache(self):
        #return self._cache

    @property
    def verbose(self):
        return self._verbose

    @property
    def deck(self) -> Deck:
        return self._deck

    @property
    def optimized(self) -> list:
        return self._optimized
    @optimized.setter
    def optimized(self, value: list):
        self._optimized = value

    """
    @permitted_lands.setter
    def permitted_lands(self, value: list):
        self._permitted_lands = value

    """
    @property
    def remaining(self) -> int:
        return self._remaining
    @remaining.setter
    def remaining(self, value: int):
        self._remaining = value


    @property
    def basics(self) -> list[Land]:
        return [x for x in self.card_list if isinstance(x, BasicLand)]


    @property
    def budget(self) -> float:
        return self._budget
    @budget.setter
    def budget(self, value:float):
        self._budget = value

    @property
    def mppc(self) -> float:
        return self._mppc
    @mppc.setter
    def mppc(self, value:float):
        self._mppc = value

    @property
    def currency(self) -> str:
        return self._currency
    @currency.setter
    def currency(self, value:str):
        self._currency = value

    @property
    def threshold(self) -> int:
        return self._threshold
    @threshold.setter
    def threshold(self, value:int):
        self._threshold = value

    @property
    def minbasics(self) -> int:
        return self._minbasics
    @minbasics.setter
    def minbasics(self, value:int):
        self._minbasics = value

    #pseudosetters


    #deck attribute setup functions
    def setup(self):
        self._colorless_pips = self.deck.colorless_pips
        self._pie_slices = self.deck.pie_slices
        self._categories = [["SearchLand"]]
        self._minbasics = 0

    def check_identity(self, card) -> bool:
        if not self.deck.format.color_id:
            return True
        for color in list(card.color_identity):
            if color not in self.deck.colors_needed:
                return False
        return True

    def vprint(self, text):
        if self.verbose:
            print(text)


    def fill_heap_CONDEMNED(self, from_testlist=None):
        if from_testlist is None:
            self.card_list = []
            all = db.session.query(Card).filter(Card._overall_land == True).all()
            lands = []
            basics = []
            for card in all:
                tp = card.true_produced
                if not self.check_identity(card):
                    pass
                elif card.cycle.name == "Basic Lands":
                    if card.produced[0] in self.deck.colors_needed:
                        self.card_list.append(self.parse_GameCard(card))
                elif len(tp) != 0:
                    match = 0
                    for color in tp:
                        if color in self.deck.colors_needed:
                            match += 1
                        if match >= 2:
                            self.card_list.append(self.parse_GameCard(card))
                            break
            #print(f"Set heap with a total of {len(self.card_list)} cards.")
        else:
            as_cards = (self.parse_cards_from_json(from_testlist))
            self.card_list = [self.parse_GameCard(x, mandatory=True) for x in as_cards]
            #for card in self.card_list:
                #print(f"{card.name}:{isinstance(card, Land)}")
        #self.heap = lands
        #self.basics = basics


    #requirements setting functions
    def set_requirements(self, budget=None, mppc=None, currency=None, threshold=None, minbasics=0):
        self.budget = self.set_if_not_none(float(budget), self.budget)
        self.mppc = self.set_if_not_none(float(mppc), self.mppc)
        self.currency = self.set_if_not_none(currency, self.currency)
        self.threshold = self.set_if_not_none(int(threshold), self.threshold)
        self.minbasics = self.set_if_not_none(int(minbasics), self.minbasics)

        
    
    def set_if_not_none(self, value, target):
        if value is None:
            return target
        return value



    #session variable functions
    def card_below_max(self, card:GameCard) -> bool:
        attribute_conversion = {
            "GBP": card.usd, #YEAH LEAH THIS IS A STOPGAP
            "USD": card.usd,
            "EUR": card.eur
        }
        cost = attribute_conversion[self.currency]
        return float(cost) <= self.mppc


    def reset_session(self):
        #self.permitted_lands = self.winnow_by_price()
        self.winnow_by_price()
        self.remaining = self.deck.lands_requested
        self.optimized = []


    def winnow_by_price(self):# -> list[GameCard]:
        if self.mppc == 0 or self.mppc is None:
            return self.card_list
        else:
            for c in self.card_list:
                if self.card_below_max(c):
                    c.permitted = False
            #return [c for c in self.card_list if self.card_below_max(c)]



    #simulation functions
    def add_to_sample(self, card:GameCard):
        copy = deepcopy(card)
        copy.zone = "deck"
        self._optimized.append(copy)
        self.remaining -= 1

    def recall_sample(self):
        l = [c for c in self.deck.card_list]
        for card in l:
            if not card.mandatory:
                self.deck.give(self, card)

    def set_sample(self):
        #curently pays no attention to minbasics, or allows for duplicates
        p = self.permitted_lands()
        random.shuffle(p) #SCAFFOLD just doing it randomly for now
        i = 0 #hey this doesn't allow for the edge case where a deck is big enough to need more lands then we have to offer
        while not self.deck.full():
            self.give(self.deck, p[i])
            i += 1

        """
        output = []
        for i in range(0, self.minbasics):
            len = len(self.basics)
            self.add_to_sample(self.basics[i % len])
        sp = random.shuffle(self.permitted_lands)
        i = 0
        while self.remaining > 0:
            self.add_to_sample(sp[i])
            i += 1

        """
    def run_CONDEMNED(self) -> dict:
        self.reset_session()
        self.run_tests()

        cards = self.output_cards()
        metrics = self.output_metrics()
        output = {
            "cards": cards,
            "metrics": metrics
        }
        return output

    def run_tests(self):
        #print("Running tests")
        temp_count = 5
        for i in range(0, 1):#SCAFFOLD
            self.set_sample()
            t = Test(self.deck, self.cache, close_examine=self._close_examine, timer=self._timer)
            t.run_deck_test()
            self.recall_sample()

    def output_cards(self) -> list[str]:
        for i in range(0, self.minbasics):
            len = len(self.basics)
            self.add_to_sample(self.basics[i % len])
        p = self.permitted_lands()
        random.shuffle(p)
        i = 0
        pass
        """        while self.remaining > 0:
            self.add_to_sample(p[i])
            i += 1

        return [x.name for x in self.optimized]
        """

    def output_metrics(self) -> dict:
        pass

    #below are versions of all of the above but just designed for testing with, not designed to be user friendly

    def dev_run(self, **kwargs):
        self.start_time = time.time()
        self.fill_heap() #get all possible lands for that deck
        self.deck.add_initial_lands("equal_basics")
        #add to the deck an initial set of lands - make this a function so you can try out different initial sets
            #ponder: what if it was all wastes? That'd certainly make your early interventions much more fiery.
        self.deck.set_each( kwargs["of_each_basic"])
        if kwargs["min_basics"] is not None:
            self.minbasics = kwargs["min_basics"]
        self.hill_climb()

    def run(self, **kwargs):
        self.add_mandatory_lands()
        self.deck.add_initial_lands("equal_basics")
        # add to the deck an initial set of lands - make this a function so you can try out different initial sets
        # ponder: what if it was all wastes? That'd certainly make your early interventions much more fiery.
        self.deck.set_each(kwargs["of_each_basic"])
        if kwargs["min_basics"] is not None:
            self.minbasics = kwargs["min_basics"]
        self.hill_climb()

    def add_mandatory_lands(self):
        giftbasket = []
        for card in self.card_list:
            if isinstance(card, Land) and card.mandatory:
                giftbasket.append(card)
        for card in giftbasket:
            self.give(self.deck, card)
            self.deck.lands_requested -= 1




    @functimer_once
    def hill_climb(self):
        self.halt = False
        step_output = Test(self.deck)
        print(f"Excluded: {[x.name for x in self.card_list if not x.permitted]}")
        print(f"Mandatory: {[x.name for x in self.card_list if x.mandatory]}")
        step_output.hill_climb_test()
        self.vprint(f"Starting score: {step_output.game_proportions}")
        scores = []
        scores.insert(0, step_output.game_proportions)
        iterations = 0
        while not self.halt:
            iterations += 1
            print(f"Iteration {iterations}")
            step_output = self.hill_climb_increment(step_output)
            #scores.insert(0, step_output.game_proportions)
            scores.append(step_output.game_proportions)
            self.halt = self.check_rolling_max(scores)
            #halt = self.check_for_halt(scores, step_output)
            if self.halt or iterations > 50:
                print(f"Halting at step {iterations}")

        self.deck.finalscore = step_output.game_proportions
        self.print_results(step_output)
        self.dev_assess_results()
        print(f"Took {iterations} iterations")

    def check_for_plateau(self, scores):
        savgol_window_length = 9
        window_length = 7
        minimum = max(window_length, savgol_window_length)

        if len(scores) < minimum or len(scores) < savgol_window_length:
            return False

        smoothed = savgol_filter(scores, window_length=savgol_window_length, polyorder=3)
        derivative = np.gradient(smoothed)
        threshold = 0.001
        min_fraction = 0.45
        for i in range(window_length, len(derivative)):
            window = derivative[i-window_length + 1:i+1]
            flat_num = sum(abs(d) < threshold for d in window)
            flat_frac = flat_num / window_length
            with open("Rukarumel_Derivatves", "a") as file:
                file.write(f"{flat_frac}\n")
            if flat_frac >= min_fraction:
                return True

        return False

    def check_for_plateau_v2(self, scores, threshold=0.001, window_length=7, min_fraction=0.7):
        savgol_window_length = 9
        poly_order = 3
        minimum = max(window_length, savgol_window_length)

        if len(scores) < minimum:
            return False

        # Smooth the scores
        smoothed = savgol_filter(scores, window_length=savgol_window_length, polyorder=poly_order)

        # Smooth the derivative
        derivative = np.gradient(smoothed)
        derivative_smoothed = savgol_filter(derivative, window_length=5, polyorder=2)

        for i in range(window_length, len(derivative_smoothed)):
            window = derivative_smoothed[i - window_length + 1:i + 1]
            flat_num = sum(abs(d) < threshold for d in window)
            flat_frac = flat_num / window_length

            # Debug print if needed
            # print(f"i={i}, flat_frac={flat_frac:.2f}, window={window}")

            if flat_frac >= min_fraction:
                return True

        return False

    def check_rolling_max(self, scores, window_size=10, improvement_threshold=0.05):
        if len(scores) < window_size *2:
            return False

        prior_window = scores[len(scores) - 2 * window_size: len(scores) - window_size]
        recent_window = scores[len(scores) - window_size:]

        best_recent = max(recent_window)
        best_prior = max(prior_window)

        #with open("Rukarumel_Performance", "a") as file:
            #file.write(f"recent: {recent_window} prior: {prior_window}\n")

        improvement = best_recent - best_prior

        # Debug print to visualize what’s going on
        print(f"Best recent: {best_recent:.3f}, Best prior: {best_prior:.3f}, Improvement: {improvement:.4f}")

        return improvement < improvement_threshold

    def dev_assess_results(self):
        lands = self.deck.lands_list()
        print(f"Fetches: {[x for x in lands if isinstance(x, FetchLand)]}")
        print(f"Shocks: {[x for x in lands if isinstance(x, ShockLand)]}")
        print(f"Fasts: {[x for x in lands if isinstance(x, FastLand)]}")
        print(f"Guildgates: {[x for x in lands if isinstance(x, GuildGate)]}")
        print(f"Bonds: {[x for x in lands if isinstance(x, BondLand)]}")
        print(f"Filters {[x for x in lands if isinstance(x, FilterLand)]}")
        print(f"Verges: {[x for x in lands if isinstance(x, Verge)]}")

        print(f"Checks: {[x for x in lands if isinstance(x, CheckLand)]}")
        print(f"Slows: {[x for x in lands if isinstance(x, SlowLand)]}")
        print(f"Snarls: {[x for x in lands if isinstance(x, RevealLand)]}")
        print(f"Pains: {[x for x in lands if isinstance(x, PainLand)]}")
        print(f"Horizons: {[x for x in lands if isinstance(x, HorizonLand)]}")
        print(f"Triomes: {[x for x in lands if isinstance(x, Triome)]}")

        #print(f"Swapped nonbasics: {[self.swapped_out_nonbasics]}")
        print(f"Totalbasics {len([x for x in lands if isinstance(x, BasicLand)])}:")
        for x in lands:
            if isinstance(x, BasicLand):
                print(f"\t{x.name}")



    def print_results(self, step_output, error=None):
        if error is not None:
            print(f"ERROR: {error}")

        step_output.print_deck_details("proportion_of_games")
        step_output.print_list(self.deck.lands_list())


    def check_for_halt(self, scores, test) -> bool:
        if self.halt:
            print("Halting")
            return True
        else:
            return False

        #if test.like_for_like:
            #return True

        """success_number = 7
        meaningless_improvement = 0.02
        give_up_number = 200
        l = len(scores)

        if l > give_up_number:
            self.vprint(f"Giving up after {l} tries")
            return True

        if l < success_number:
            return False

        i = 0
        to_test = []
        while i < success_number:
            to_test.append(scores[i])
            i += 1

        maxi = max(to_test)
        mini = min(to_test)

        return maxi - mini <= meaningless_improvement"""

    #@functimer_once
    @functimer_once
    def hill_climb_increment(self, prior_test):
        print("")
        worst_card = prior_test.worst_performing_card
        prev_score = prior_test.game_proportions
        if not isinstance(worst_card, BasicLand):
            self.swapped_out_nonbasics.append(worst_card)


        t = Test(self.deck)
        if self.meets_minbasic_criteria(worst_card):
            cards_to_test = self.get_basic_spread()
        else:
            cards_to_test = self.get_cards_to_test()
        self.deck.give(self, worst_card)

        champ = None
        tested_cards = []
        for trial_card in cards_to_test:
            self.give(self.deck, trial_card)
            trial_card.card_test_score = t.run_card_test(trial_card)
            self.deck.give(self, trial_card)
            if champ is None or trial_card.card_test_score > champ.card_test_score:
                champ = trial_card
            tested_cards.append(trial_card)

        tested_cards.sort(key=lambda x: x.card_test_score, reverse=True)
        tiebreaker_candidates = []
        for card in tested_cards:
            if card.card_test_score >= champ.card_test_score - 0.01:
                tiebreaker_candidates.append(card)
            else:
                break


        for c in tested_cards:
            print(f"\t{c} -> {c.card_test_score} ({median(c.options)})")

        champ = self.break_tie(tiebreaker_candidates)
        #champ = self.break_tie_median(tiebreaker_candidates)

        #if champ.card_test_score < prev_score:
            #print(f"Halting at prior test score {prior_test.game_proportions}")
            #self.halt = True

        if not self.halt:
            self.give(self.deck, champ)
            self.reset_scores(cards_to_test)
            t.hill_climb_test()
            self.vprint(f"Swapped {worst_card} for {champ} ({t.game_proportions})")
            #with open("another rukarumeeel", "a") as file:
                #print("Writing to file!")
                #file.write(f"{t.game_proportions}\n")

            if worst_card.name == champ.name:
                t.like_for_like = True
        #print(f"total of {(time.time() - self.start_time)/60} minutes elapsed")
        return t

    def meets_minbasic_criteria(self, card):
        if not isinstance(card, BasicLand):
            return False

        basic_count = 0
        for card in self.deck.card_list:
            if isinstance(card, BasicLand):
                basic_count += 1

        return basic_count <= self.minbasics

    def break_tie(self, candidates):
        if len(candidates) == 1:
            return candidates[0]

        output = max(candidates, key=lambda x: numpy.median(x.options))

        if output != candidates[0]:
            print(f"Shifting {output} ({float(numpy.mean(output.options))}) ahead of {candidates[0]} ({float(numpy.mean(candidates[0].options))})")

        return output

    def break_tie_median(self, candidates):
        if len(candidates) == 1:
            return candidates[0]

        output = max(candidates, key=lambda x: x.card_test_score)

        if output != candidates[0]:
            print(
                f"Shifting {output} ({float(numpy.mean(output.options))}) ahead of {candidates[0]} ({float(numpy.mean(candidates[0].options))})")

        return output



    def get_cards_to_test(self) -> list:
        uniques = self.get_unique_cards()
        output = []
        for card in uniques:
            if not any(superior not in self.deck.card_list for superior in card.superior_lands):
                output.append(card)



        """output = self.get_unique_cards()

        for slice in self.pie_slices:
            output = self.enqueue_category(slice, output)
        for category in self.categories:
            output = self.enqueue_category(category, output)
        #print(f"First output: {output}")
        return output"""
        return output


    def enqueue_category(self, category, lands):
        #print(f"category: {category} lands: {lands}")
        try:
            front = min((x.priority for x in lands if self.ranking_equivalence(x, category)))
            output = [x for x in lands if not self.ranking_equivalence(x, category) or x.priority == front]
            return output
        except ValueError:
            return lands

    def ranking_equivalence(self, land, category):
        sland = sorted(land.ranking_category(self))
        scat = sorted(category)
        output = sland == scat
        return output







    def get_unique_cards(self, only_permitted=True) -> list:
        cardlist = []
        basicnames = []

        if not only_permitted:
            selection = self.card_list
        else:
            selection = self.permitted_lands()

        for card in selection:
            if card.name not in basicnames:
                cardlist.append(card)
            if isinstance(card, BasicLand) and card.name not in basicnames:
                if card.name != "Wastes" and not self.colorless_pips:
                    basicnames.append(card.name)
        return cardlist

    def reset_scores(self, input):
        for item in input:
            item.card_test_score = None

    def dev_fill_heap(self, deckname):
        match deckname:
            case _:
                heap = "Zagoth Triome\nDarkslick Shores\nBotanical Sanctum\nBlooming Marsh\nUnderground River\nYavimaya Coast\nLlanowar Wastes\nDimir Guildgate\nSimic Guildgate\nGolgari Guildgate\nShipwreck Marsh\nDreamroot Cascade\nDeathcap Glade\nChoked Estuary\nVineglimmer Snarl\nNecroblossom Snarl\nWatery Grave\nBreeding Pool\nOvergrown Tomb\nDrowned Catacomb\nHinterland Harbor\nWoodland Cemetery\nSunken Hollow\nPolluted Delta\nMisty Rainforest\nVerdant Catacombs\nWaterlogged Grove\nNurturing Peatland\nMorphic Pool\nRejuvenating Springs\nUndergrowth Stadium\nCommand Tower"

                #currently default is Xavier Sal


        as_cards = self.parse_cards_from_json(heap)
        self.card_list = [self.parse_GameCard(x, mandatory=False) for x in as_cards]

    def fill_heap(self):
        all = db.session.query(Card).filter(Card._overall_land == True).all()
        for card in all:
            if self.deck.within_color_identity(card):
                as_GC = self.parse_GameCard(card, mandatory=False)
                #self.prioritization_object.register_land(as_GC)
                if not isinstance(as_GC, MiscLand) and not self.irrelevant_fetchland(as_GC, exclude_offcolors=False):
                    self.card_list.append(as_GC)
                    if self.irrelevant_fetchland(as_GC, exclude_offcolors=True):
                        as_GC.off_color_fetch = True

        #for card in self.deck.lands_list():
            #self.prioritization_object.register_land(card)
        #self.prioritize_heap()

    def prioritize_heap(self):
        permitted = self.permitted_lands()
        for land in permitted:
            self.prioritization_object.register_land(land)

        for land in permitted:
            land.superior_lands = self.prioritization_object.cascade_superiors(land, self.deck)


    def prioritize_heap_CONDEMNED(self, prioritization:dict):
        for land in self.card_list:
            land.priority = prioritization[land.cycle]

    def prioritize_heap_CONDEMNED_2(self):
        heap = self.lands_list()
        for land in heap:
            all_except = [x for x in heap if x != land and len(list(set(land.heap_prod(self.deck)) - set(x.heap_prod(self.deck)))) == 0]
            for candidate in all_except:
                if any(isinstance(candidate, cls) for cls in land.superior_classes):
                    land.superior_lands.append(candidate)
            print(f"{land} has superiors {land.superior_lands}")
        self.card_list = [x for x in heap if x.name != "Wastes" and not self.colorless_pips]








    def irrelevant_fetchland(self, card, exclude_offcolors = False):
        if not isinstance(card, FetchLand):
            return False
        if exclude_offcolors:
            for landtype in card.searchable:
                if colortype_map[landtype] not in self.deck.colors_needed:
                    return True
            return False
        for landtype in card.searchable:
            if colortype_map[landtype] in self.deck.colors_needed:
                return False
        return True








    """    def fill_heap_CONDEMNED(self, from_testlist=None):
        if from_testlist is None:
            self.card_list = []
            all = db.session.query(Card).filter(Card._overall_land == True).all()
            lands = []
            basics = []
            for card in all:
                tp = card.true_produced
                if not self.check_identity(card):
                    pass
                elif card.cycle.name == "Basic Lands":
                    if card.produced[0] in self.deck.colors_needed:
                        self.card_list.append(self.parse_GameCard(card))
                elif len(tp) != 0:
                    match = 0
                    for color in tp:
                        if color in self.deck.colors_needed:
                            match += 1
                        if match >= 2:
                            self.card_list.append(self.parse_GameCard(card))
                            break
            #print(f"Set heap with a total of {len(self.card_list)} cards.")
        else:
            as_cards = (self.parse_cards_from_json(from_testlist))
            self.card_list = [self.parse_GameCard(x, mandatory=True) for x in as_cards]
            #for card in self.card_list:
                #print(f"{card.name}:{isinstance(card, Land)}")
        #self.heap = lands
        #self.basics = basics"""

    #SIMULATED ANNEALING DEMO
    def simulated_annealing_method(self):
        self.fill_heap()
        self.add_max_basics()
        """self.shuffle()
        for i in range(self.deck.lands_requested):
            self.give_top(self.deck)"""
        self.fill_deck_and_canister(self.deck.lands_requested)
        halt = False
        temperature = 0.75
        scoreboard = []
        t = Test(self.deck, self.cache, close_examine=self._close_examine, timer=self._timer)
        t.run_tests()
        t.assess_deck_hc()
        while not halt:
            t = self.anneal(temperature, t)
            print(f"Score of {t.game_proportions}")
            scoreboard.append(t.game_proportions)
            temperature *= 0.9
            if len(scoreboard) == 30:
                halt = True
        print(f"Scoreboard: {scoreboard}")
        for card in self.deck.lands_list():
            print(card)


    def random_deck_fill(self, count):
        pass

    def anneal(self, temperature, mastertest):
        print("")
        #mastertest = Test(self.deck, self.cache, close_examine=self._close_examine, timer=self._timer)
        #mastertest.run_tests()
        #mastertest.assess_deck_hc()
        sorted_lands = sorted(self.deck.lands_list(), key=lambda x: x.proportion_of_games(), reverse=False)
        print(sorted_lands)
        quant = round(temperature * len(sorted_lands))


        print(f"Mastertest output {mastertest.game_proportions}")
        i = 0
        for land in sorted_lands:
            if i == quant:
                print("----SAFETY ZONE----")
            print(f"\t{i}:{land} -> {land.proportions}")
            land.reset_grade()
            i += 1

        low_scorers = []
        for i in range(quant):
            low_scorers.append(sorted_lands[i])
            self.deck.card_list.remove(sorted_lands[i])

        give_up = 0

        while give_up < 100:
            """self.shuffle()
            canister = []
            for _ in range(quant):
                topcard = self.card_list.pop()
                canister.append(topcard)
                self.deck.card_list.append(topcard)"""
            canister = self.fill_deck_and_canister(quant)
            subtest = Test(self.deck, self.cache, close_examine=self._close_examine, timer=self._timer)
            subtest.run_tests()
            subtest.assess_deck_hc()
            if subtest.game_proportions > mastertest.game_proportions:
                print(f"New list bumped up to {subtest.game_proportions}")
                for card in canister:
                    print(f"\t{card}")
                for card in low_scorers:
                    self.card_list.append(card)
                return subtest
            else:
                for land in self.deck.lands_list():
                    land.reset_grade()
                for card in canister:
                    self.deck.give(self, card)
                give_up += 1
                if give_up == 30:
                    print("Tried 30 times...")
                if give_up == 60:
                    print("Tried 60 times...")
                if give_up == 90:
                    print("Only going to try this ten more times...")

        print(f"No improvement recorded")
        for card in low_scorers:
            self.deck.card_list.append(card)
        self.dev_assess_results()
        raise Exception("Stop!")
        #return mastertest

    def fill_deck_and_canister(self, quant_needed):
        removed_basics = self.restrict_basics(quant_needed)
        #print(f"Removing basics and left with {len(self.card_list)} cards")
        self.shuffle()
        obtained = 0
        i = 0

        output = []
        while obtained < quant_needed:
            candidate = self.card_list[i % len(self.card_list)]
            if not any(superior not in self.deck.card_list for superior in candidate.superior_lands):
                output.append(candidate)
                self.give(self.deck, candidate)
                obtained += 1
            else:
                i += 1
            if i > 1000:
                raise Exception("fill_deck_and_canister having the issue you thought it might")
        for land in removed_basics:
            self.card_list.append(land)
        return output

    def restrict_basics(self, quant):
        furtherquant = ceil(quant / 2)
        bank = {"Plains":0,
                "Island":0,
                "Swamp":0,
                "Mountain":0,
                "Forest":0,
                "Wastes": 0
                }
        output = []
        for card in self.card_list:
            if isinstance(card, BasicLand):
                bank[card.name] += 1
                if bank[card.name] >= furtherquant:
                    self.card_list.remove(card)
                    output.append(card)
        return output

    def add_max_basics(self):
        quant = self.deck.lands_requested - 1
        for color in self.deck.colors_needed:
            sought_land = [x for x in self.card_list if x.name == landtype_map[color]][0]
            for _ in range(quant):
                self.card_list.append(deepcopy(sought_land))

    def set_rankings(self, rankings):
        new_rankings = []
        for r in rankings:
            as_list = []
            cycles = rankings[r]
            for cycle in cycles:
                name = cycle["typeName"]
                as_list.append(name)
            new_rankings.append(as_list)

        print(f"New rankings: {new_rankings}")



        self.prioritization_object.apply_player_rankings(new_rankings)
        self.prioritize_heap()

























