from simulation_objects.GameCard import GameCard

class Spell(GameCard):
    def __init__(self, name, zone):
        GameCard.__init__(self, name, zone)
