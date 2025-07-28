
import random
from copy import deepcopy

import numpy
from numpy.ma.core import set_fill_value

from database_management.models.Card import Card
from Extensions import db
from math import inf

from simulation_objects.CardCollections.CardCollection import CardCollection
from simulation_objects.CardCollections.Deck import Deck
from simulation_objects.GameCards import FastLand, ShockLand, MiscLand, BondLand, CheckLand, SlowLand, RevealLand, \
    PainLand, HorizonLand
from simulation_objects.GameCards.BasicLand import BasicLand
from simulation_objects.GameCards.GameCard import GameCard
from simulation_objects.GameCards.Land import Land
from simulation_objects.GameCards.SearchLands.FetchLand import FetchLand
from simulation_objects.GameCards.TappedCycles.GuildGate import GuildGate
from simulation_objects.GameCards.TappedCycles.Triome import Triome
from simulation_objects.Misc.ColorPie import colortype_map
from simulation_objects.Simulations.Test import Test
from simulation_objects.Misc.LandPermutationCache import LandPermutationCache
from simulation_objects.Timer import functimer_perturn, functimer_once


class MonteCarlo(CardCollection):
    def __init__(self, deck, close_examine=False, timer=False, verbose=False):
        CardCollection.__init__(self)
        #set on creation of the object
        self._deck = deck
        self._cache = LandPermutationCache()
        self._colorless_pips = deck.colorless_pips
        self._pie_slices = self.deck.pie_slices
        self._categories = [["SearchLand"]]
        
        self.halt = False

        #will figure out when to set the below
        self._prioritization= {
            "Command Tower": 1,
            "Triomes": 1,
            "Shock Lands": 1,
            "Basic Lands": 1,
            "OG Dual Lands": 1,
            "Fetch Lands": 1,
            "Tri-Color Taplands": 2,
            "Bond Lands": 2,
            "Pain Lands": 2,
            "Horizon Lands": 2,
            "Check Lands": 3,
            "Reveal Lands": 3,
            "Battle Lands": 3,
            "Fast Lands": 3,
            "Slow Lands": 3,
            "Guildgates": 4
        }


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

    @property
    def cache(self):
        return self._cache

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
    def permitted_lands(self) -> list:
        #return self._permitted_lands
        return [c for c in self.card_list if c.permitted]

    #deck attribute setup functions
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
    def run(self) -> dict:
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

    def dev_run(self):
        self.fill_heap() #get all possible lands for that deck
        self.deck.add_initial_lands("proportional_basics")
        #add to the deck an initial set of lands - make this a function so you can try out different initial sets
            #ponder: what if it was all wastes? That'd certainly make your early interventions much more fiery.
        self.hill_climb()


    @functimer_once
    def hill_climb(self):
        halt = False
        step_output = Test(self.deck, self.cache)
        step_output.hill_climb_test()
        self.vprint(f"Starting score: {step_output.game_proportions}")
        scores = []
        scores.insert(0, step_output.game_proportions)
        iterations = 0
        while not halt:
            iterations += 1
            step_output = self.hill_climb_increment(step_output)
            scores.insert(0, step_output.game_proportions)
            halt = self.check_for_halt(scores, step_output)
        self.print_results(step_output)
        self.dev_assess_results()
        print(f"Took {iterations} iterations")

    def dev_assess_results(self):
        lands = self.deck.lands_list()
        print(f"Fetches: {[x for x in lands if isinstance(x, FetchLand)]}")
        print(f"Shocks: {[x for x in lands if isinstance(x, ShockLand)]}")
        print(f"Fasts: {[x for x in lands if isinstance(x, FastLand)]}")
        print(f"Guildgates: {[x for x in lands if isinstance(x, GuildGate)]}")
        print(f"Bonds: {[x for x in lands if isinstance(x, BondLand)]}")

        print(f"Checks: {[x for x in lands if isinstance(x, CheckLand)]}")
        print(f"Slows: {[x for x in lands if isinstance(x, SlowLand)]}")
        print(f"Snarls: {[x for x in lands if isinstance(x, RevealLand)]}")
        print(f"Pains: {[x for x in lands if isinstance(x, PainLand)]}")
        print(f"Horizons: {[x for x in lands if isinstance(x, HorizonLand)]}")
        print(f"Triomes: {[x for x in lands if isinstance(x, Triome)]}")

        print(f"Swapped nonbasics: {[self.swapped_out_nonbasics]}")
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
            return True

        #if test.like_for_like:
            #return True

        success_number = 5
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

        return maxi - mini <= meaningless_improvement

    @functimer_once
    def hill_climb_increment(self, prior_test):
        print("")
        print(f"Cache at length {len(self.cache.cache)}")
        worst_card = prior_test.worst_performing_card
        prev_score = prior_test.game_proportions
        if not isinstance(worst_card, BasicLand):
            self.swapped_out_nonbasics.append(worst_card)


        t = Test(self.deck, self.cache)
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
            print(f"\t{c} -> {c.card_test_score} ({numpy.mean(c.options)})")

        if champ.card_test_score < prev_score:
            self.halt = True

        champ = self.break_tie(tiebreaker_candidates)


        self.give(self.deck, champ)
        self.reset_scores(cards_to_test)
        t.hill_climb_test()
        self.vprint(f"Swapped {worst_card} for {champ} ({t.game_proportions})")
        self.cache.compare()
        if worst_card.name == champ.name:
            t.like_for_like = True
        return t

    def break_tie(self, candidates):
        if len(candidates) == 1:
            return candidates[0]


        output = max(candidates, key=lambda x: numpy.mean(x.options))

        if output != candidates[0]:
            print(f"Shifting {output} ({float(numpy.mean(output.options))}) ahead of {candidates[0]} ({float(numpy.mean(candidates[0].options))})")

        return output



    def get_cards_to_test(self) -> list:
        output = self.get_unique_cards()

        for slice in self.pie_slices:
            output = self.enqueue_category(slice, output)
        for category in self.categories:
            output = self.enqueue_category(category, output)
        #print(f"First output: {output}")
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







    def get_unique_cards(self) -> list:
        cardlist = []
        basicnames = []
        for card in self.card_list:
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
                if not isinstance(as_GC, MiscLand) and not self.irrelevant_fetchland(as_GC, exclude_offcolors=True):
                    self.card_list.append(as_GC)

        self.prioritize_heap(self.prioritization)

        self.print_all()

    def prioritize_heap(self, prioritization:dict):
        for land in self.card_list:
            land.priority = prioritization[land.cycle]


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




















