from simulation_objects.GameCards.FilterLands.RampLand import RampLand


class BounceLand(RampLand):

    def conditions(self, game):
        #print(f"{self.name} produces {str(self.produced)}")
        output = [{
            "land":self,
            "color": self.produced,
            "pain": None,
            "sac": None

        }]

        #print(f"{self} can produce {len(output)} mana")
        return output

    def tap_specific(self, game, color):
        if color != self.live_prod(game):
            raise Exception(f"{self.name} should not tap for {color}")
        self.tapped = True
