from simulation_objects.GameCards.GameCard import GameCard
import simulation_objects.Simulations as Simulations
import simulation_objects.CardCollections as CardCollections


class Land(GameCard):
    def __init__(self, card, mandatory=False):
        GameCard.__init__(self, card, mandatory)
        self._produced = list(card.produced)

    @property
    def produced(self) -> list[str]:
        return self._produced


    #pseudogetters
    def live_prod(self, deck:CardCollections.Deck) -> list[str]:
        return self._produced


    def conditions(self, deck:CardCollections.Deck):
        #print(f"{self.name} produces {str(self.produced)}")
        output = []
        for color in self.live_prod(deck):
            dict = {
                "color": color,
                "pain": None,
                "sac": None,
            }
            output.append(dict)
        print(f"{self} can produce {len(output)} mana")
        return output




