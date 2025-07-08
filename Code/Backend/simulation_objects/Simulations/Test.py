#from simulation_objects.CardCollections.Deck import Deck
from simulation_objects.Simulations.Game import Game
from simulation_objects.Simulations.Simulation import Simulation
from datetime import datetime

class Test(Simulation):
    def __init__(self, deck):
        Simulation.__init__(self, deck)

    #run!
    def run(self):
        decisions = 0
        mana_per_game = 0
        options_per_turn = 0
        for i in range(0, 10000):#SCAFFOLD - currently at 6 seconds per 10,000 games
            #if i % 100 == 0:
                #print(f"{i}...")
            g = Game(self.deck)
            g.run()
            decisions += g.decisions
            mana_per_game += (g.total_spent_mana/10000)
            options_per_turn += (g.options_per_turn/10000)
        print(f"Made a total of {decisions} decisions, spending an average of {mana_per_game} mana and having around {options_per_turn} choices each turn")