from simulation_objects.GameCards.GameCard import GameCard

class Spell(GameCard):
    def __init__(self, name, mandatory=False):
        GameCard.__init__(self, name, mandatory)
