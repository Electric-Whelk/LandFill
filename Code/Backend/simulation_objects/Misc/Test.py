#from simulation_objects.CardCollectiions.Deck import Deck
from simulation_objects.Misc.Game import Game
from simulation_objects.Misc.Simulation import Simulation

class Test(Simulation):
    def __init__(self, deck):
        Simulation.__init__(self, deck)

    #run!
    def run(self):
        for i in range(0, 10): #SCAFFOLD
            g = Game()
            g.run