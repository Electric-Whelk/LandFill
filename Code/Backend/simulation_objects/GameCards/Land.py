from simulation_objects.GameCards.GameCard import GameCard

class Land(GameCard):
    def __init__(self, card, mandatory=False):
        GameCard.__init__(self, card, mandatory)
