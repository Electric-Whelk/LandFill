from simulation_objects.GameCards.RampLands.RampLand import RampLand


class BounceLand(RampLand):
    def __init__(self, land, mandatory=False):
        RampLand.__init__(self, land, mandatory=mandatory)
        self._strobe = False

    @property
    def strobe(self):
        return self._strobe
    @strobe.setter
    def strobe(self, value):
        self._strobe = value

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

    def permatap(self) -> bool:
        return True



    def run_etb(self, game):
        target = self.find_bounce_target(game)
        game.vprint(f"Bouncing {target}")
        game.battlefield.give(game.hand, target)
        pass


    def find_bounce_target(self, game):
        not_bounceland = None
        lands_list = game.battlefield.lands_list()
        for land in lands_list:
            if land.enters_untapped(game):
                return land
            if not isinstance(land, BounceLand):
                not_bounceland = land
        if not_bounceland is None:
            return lands_list[0]
        return not_bounceland

    def set_price(self, game, color):
        #a bit janky but it should work
        #bouncelands are added to the list twice, and "strobe" back and forth between options

        if self.strobe:
            prodded = self.live_prod(game)[0]
        else:
            prodded = self.live_prod(game)[1]
        self.strobe = not self.strobe


        if color == "None":
            return self.generic_price
        if not self.tapped:
            if color == "Gen":
                return self.generic_price
            if color in self.live_prod(game):
                return self.color_price
        return 9999


