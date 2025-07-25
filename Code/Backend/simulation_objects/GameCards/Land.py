from simulation_objects.GameCards.GameCard import GameCard
#import simulation_objects.Simulations as Simulations
#from simulation_objects.CardCollections import Deck
import numpy
from scipy.stats import skew, kurtosis


class Land(GameCard):
    def __init__(self, card, mandatory=False):
        GameCard.__init__(self, card, mandatory)
        self._produced = list(card.produced)
        self._landtypes = card.subtypes
        self._permatap = False
        self._cycle = card.cycle.name
        #print(f"{self.name}:{self._landtypes}")
        #self._tp = list(card.true_produced)
        #self._produced = list(card.true_produced)
        self._grade = {"Mana": 0,
                       "Options": 0,
                       "Wasted": [],
                       "Appearances": 0}
        self._monocolor = False

        #dev attributes
        self.peek = False

        #stats attributes
        self._turn_appearances = 0
        self._wasteless_turns = 0
        self._above_average_wasteless_turns = False
        self._above_average_wasteless_games = False
        self._proportions = 0

        #monte carlo attributes
        self._card_test_score = None

    #getters and setters
    @property
    def proportions(self):
        return self._proportions
    @proportions.setter
    def proportions(self, value):
        self._proportions = value

    @property
    def cycle(self):
        return self._cycle

    @property
    def card_test_score(self):
        return self._card_test_score
    @card_test_score.setter
    def card_test_score(self, value):
        self._card_test_score = value

    @property
    def above_average_wasteless_turns(self):
        return self._above_average_wasteless_turns
    @above_average_wasteless_turns.setter
    def above_average_wasteless_turns(self, value):
        self._above_average_wasteless_turns = value

    @property
    def above_average_wasteless_games(self):
        return self._above_average_wasteless_games
    @above_average_wasteless_games.setter
    def above_average_wasteless_games(self, value):
        self._above_average_wasteless_games = value


    @property
    def turn_appearances(self) -> int:
        return self._turn_appearances
    @turn_appearances.setter
    def turn_appearances(self, value:int):
        self._turn_appearances = value

    @property
    def wasteless_turns(self) -> int:
        return self._wasteless_turns
    @wasteless_turns.setter
    def wasteless_turns(self, value:int):
        self._wasteless_turns = value

    @property
    def grade(self):
        return self._grade
    @grade.setter
    def grade(self, grade:dict):
        self._grade = grade

    @property
    def monocolor(self):
        return self._monocolor


    @property
    def produced(self) -> list[str]:
        return self._produced

    @property
    def landtypes(self) -> list[str]:
        return self._landtypes

    @property
    def permatap(self) -> bool:
        return self._permatap
    @permatap.setter
    def permatap(self, value: bool):
        self._permatap = value


    #pseudogetters
    def live_prod(self, game) -> list[str]:
        return self._produced


    #determine play state
    def ranking_category(self, monty):
        return self.produced

    def conclude_turn(self, game):
        pass

    def conditions(self, game):
        #print(f"{self.name} produces {str(self.produced)}")
        output = []
        for color in self.live_prod(game):
            dict = {
                "land": self,
                "color": color,
                "pain": None,
                "sac": None
            }
            output.append(dict)
        #print(f"{self} can produce {len(output)} mana")
        return output

    def enters_untapped(self, game) -> bool:
        return not self.permatap

    def produced_on_entry(self, game) -> list[dict]:
        if self.enters_untapped(game):
            return self.conditions(game)
        else:
            return []

    def run_etb(self, game):
        pass

    def tap_for(self, game, color):
        self.tap_specific(game, color)
        self.tap_general()


    def tap_general(self):
        #this is for stuff like logging the mana cost of the lump being cast with the land.
        pass

    def tap_specific(self, game, color):
        if color not in self.live_prod(game):
            raise Exception(f"{self.name} should not tap for {color}")
        self.tapped = True

    def increase(self, game) -> int:
        if not self.enters_untapped(game):
            return 0
        else:
            return 1

    #grade
    def award_points(self, mana, options):
        self.grade["Mana"] += mana
        self.grade["Options"] += options
        self.grade["Wasted"].append(mana)
        self.grade["Appearances"] += 1
        #if self.name == "Polluted Delta":
            #print(f"Awarding Polluted Delta {mana}")

    def reset_grade(self):
        self.grade["Mana"] = 0
        self.grade["Options"] = 0
        self.grade["Wasted"] = []
        self.grade["Appearances"] = 0
        self.wasteless_turns = 0
        self.turn_appearances = 0
        self.above_average_wasteless_games = False
        self.above_average_wasteless_turns = False
        self.proportions = 0

    def to_mean(self):
        self.grade["Mana"] /= self.grade["Appearances"]
        self.grade["Options"] /= self.grade["Appearances"]

    def wasted(self):
        return self.grade["Wasted"]

    def average_wasted(self):
        return numpy.mean(self.wasted())

    def appearances(self):
        return self.grade["Appearances"]

    def kurtosis(self):
        return kurtosis(self.wasted())

    def skew(self):
        return skew(self.wasted())

    def proportion_of_games(self):
        zeroes = len([x for x in self.wasted() if x == 0])
        try:
            output = zeroes/self.appearances()
            self.proportions = output
            return output
        except ZeroDivisionError:
            print(f"{self} did not appear in a deck test")
            self.proportions = output
            return 0.5

    def proportion_of_turns(self) -> float:
        return self.wasteless_turns/self.turn_appearances



    #overridden fuctions
    def produced_quantity(self) -> int:
        return 1

    def can_produce(self, color: str, game) -> bool:
        #this will be different for ramp/filter lands jsyk
        return color in self.live_prod(game)


    #monte carlo functions

    #Dev Functions
    def peek_board_state(self, game):
        if self.peek:
            print(f"Playing {self} with {game.hand.card_list} in hand and {game.battlefield.lands_list} in play")







