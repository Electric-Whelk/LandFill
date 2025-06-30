from simulation_objects.GameCard import GameCard

class Land(GameCard):
    def __init__(self, name, zone):
        GameCard.__init__(self, name, zone)
