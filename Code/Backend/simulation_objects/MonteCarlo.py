from abc import abstractmethod
from copy import deepcopy
from database_management.models.Card import Card
from Extensions import db
from math import inf
from random import shuffle, random

from simulation_objects.CardCollection import CardCollection
from simulation_objects.Deck import Deck
from simulation_objects.GameCard import GameCard
from simulation_objects.Land import Land
from simulation_objects.Spell import Spell

class MonteCarlo(CardCollection):
    def __init__(self, deck):
        #set on creation of the object
        self._deck = deck

        #deck attributes - set when the deck is determined
        self._heap = []
        self._basics = []


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

    @property
    def permitted_lands(self) -> list:
        return self._permitted_lands
    @permitted_lands.setter
    def permitted_lands(self, value: list):
        self._permitted_lands = value

    @property
    def remaining(self) -> int:
        return self._remaining
    @remaining.setter
    def remaining(self, value: int):
        self._remaining = value


    @property
    def basics(self) -> list[Land]:
        return self._basics
    @basics.setter
    def basics(self, value: list[Land]):
        self._basics = value

    @property
    def heap(self) -> list[GameCard]:
        return self._heap
    @heap.setter
    def heap(self, value: list[GameCard]):
        self._heap = value


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



    #deck attribute setup functions
    def check_identity(self, card) -> bool:
        if not self.deck.format.color_id:
            return True
        for color in list(card.color_identity):
            if color not in self.deck.colors_needed:
                return False
        return True



    def fill_heap(self):
        all = db.session.query(Card).filter(Card._overall_land == True).all()
        lands = []
        basics = []
        for card in all:
            tp = card.true_produced
            if not self.check_identity(card):
                pass
            elif card.cycle.name == "Basic Lands":
                if card.produced[0] in self.deck.colors_needed:
                    self._basics.append(self.parse_GameCards(card, "heap"))
            elif len(tp) != 0:
                match = 0
                for color in tp:
                    if color in self.deck.colors_needed:
                        match += 1
                    if match >= 2:
                        self._heap.append(self.parse_GameCards(card, "heap"))
                        break
        print(f"Set heap with a total of {len(self._heap)} cards.")
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
        self.permitted_lands = self.winnow_by_price()
        self.remaining = self.deck.lands_requested
        self.optimized = []


    def winnow_by_price(self) -> list[GameCard]:
        if self.mppc == 0:
            return self.heap
        else:
            return [c for c in self.heap if self.card_below_max(c)]



    #simulation functions
    def add(self, card:GameCard):
        copy = deepcopy(card)
        copy.zone = "deck"
        self._optimized.append(copy)
        self.remaining -= 1



    def run(self) -> dict:
        self.reset_session()

        cards = self.output_cards()
        metrics = self.output_metrics()
        output = {
            "cards": cards,
            "metrics": metrics
        }
        return output

    def output_cards(self) -> list[str]:
        for i in range(0, self.minbasics):
            len = len(self.basics)
            self.add(self.basics[i % len])
        shuffle(self.permitted_lands)
        i = 0
        while self.remaining > 0:
            self.add(self.permitted_lands[i])
            i += 1

        print(f"optimized: {self.optimized}")

        return [x.name for x in self.optimized]


    def output_metrics(self) -> dict:
        pass


















