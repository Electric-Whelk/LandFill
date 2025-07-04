from simulation_objects.GameCards.GameCard import GameCard
#import simulation_objects.Simulations as Simulations
#from simulation_objects.CardCollections import Deck


class Land(GameCard):
    def __init__(self, card, mandatory=False):
        GameCard.__init__(self, card, mandatory)
        self._produced = list(card.produced)

    @property
    def produced(self) -> list[str]:
        return self._produced


    #pseudogetters
    def live_prod(self, game) -> list[str]:
        return self._produced


    def conditions(self, game):
        #print(f"{self.name} produces {str(self.produced)}")
        output = []
        for color in self.live_prod(game):
            dict = {
                "land": self,
                "color": color,
                "pain": None,
                "sac": None,
            }
            output.append(dict)
        #print(f"{self} can produce {len(output)} mana")
        return output




