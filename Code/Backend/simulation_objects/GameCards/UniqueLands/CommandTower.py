from .UniqueLand import UniqueLand
#from simulation_objects.CardCollections import Deck


class CommandTower(UniqueLand):
    def __init__(self, card, mandatory=False):
        UniqueLand.__init__(self, card, mandatory=mandatory)


    def live_prod(self, game) -> list[str]:
        return game.deck.color_id

    def ranking_category(self, monty):
        return monty.deck.color_id