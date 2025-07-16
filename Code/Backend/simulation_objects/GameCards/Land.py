from simulation_objects.GameCards.GameCard import GameCard
#import simulation_objects.Simulations as Simulations
#from simulation_objects.CardCollections import Deck


class Land(GameCard):
    def __init__(self, card, mandatory=False):
        GameCard.__init__(self, card, mandatory)
        self._produced = list(card.produced)
        self._landtypes = card.subtypes
        self._permatap = False
        #print(f"{self.name}:{self._landtypes}")
        #self._tp = list(card.true_produced)
        #self._produced = list(card.true_produced)
        self._grade = {"Mana": 0,
                       "Options": 0,
                       "Appearances": 0}
        self._monocolor = False

        #dev attributes
        self.peek = False

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
        self.grade["Appearances"] += 1

    def reset_grade(self):
        for item in self.grade:
            self.grade[item] = 0

    def to_mean(self, runs):
        self.grade["Mana"] /= self.grade["Appearances"]
        self.grade["Options"] /= self.grade["Appearances"]

    #overridden fuctions
    def produced_quantity(self) -> int:
        return 1

    #Dev Functions
    def peek_board_state(self, game):
        if self.peek:
            print(f"Playing {self} with {game.hand.card_list} in hand and {game.battlefield.lands_list} in play")





