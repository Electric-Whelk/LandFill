
import random
from copy import deepcopy
from database_management.models.Card import Card
from Extensions import db
from math import inf

from simulation_objects.CardCollections.CardCollection import CardCollection
from simulation_objects.CardCollections.Deck import Deck
from simulation_objects.GameCards.BasicLand import BasicLand
from simulation_objects.GameCards.GameCard import GameCard
from simulation_objects.GameCards.Land import Land
from simulation_objects.Simulations.Test import Test


class MonteCarlo(CardCollection):
    def __init__(self, deck):
        CardCollection.__init__(self)
        #set on creation of the object
        self._deck = deck


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


    #setters and getters
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


    def fill_heap(self, from_testlist=None):
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
        print("Running tests")
        temp_count = 5
        for i in range(0, 1):#SCAFFOLD
            self.set_sample()
            t = Test(self.deck)
            t.run()
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


















