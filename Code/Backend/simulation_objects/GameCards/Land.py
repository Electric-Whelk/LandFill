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





