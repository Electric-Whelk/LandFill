#from simulation_objects.CardCollections.Deck import Deck
from simulation_objects.Simulations.Game import Game
from simulation_objects.Simulations.Simulation import Simulation

class Test(Simulation):
    def __init__(self, deck):
        Simulation.__init__(self, deck)

    #run!
    def run(self):
        for i in range(0, 10000):#SCAFFOLD
            if i % 100 == 0:
                print(f"{i}...")
            g = Game(self.deck)
            g.run()