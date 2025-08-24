from .UniqueLand import UniqueLand
#from simulation_objects.CardCollections import player_deck


class CommandTower(UniqueLand):
    def __init__(self, card, mandatory=False, **kwargs):
        UniqueLand.__init__(self, card, mandatory=mandatory, **kwargs)


    def live_prod(self, game) -> list[str]:
        return game.deck.color_id

    def heap_prod(self, deck):
        return deck.color_id

    def ranking_category(self, monty):
        return monty.deck.color_id