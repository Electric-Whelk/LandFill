from simulation_objects.GameCards.UntappableCycles.UntappableLand import UntappableLand

class PainLand(UntappableLand):
    pass

    def heap_prod(self, deck):
        if deck.colorless_pips:
            return self.produced
        else:
            return [color for color in self.produced if color != "C"]

