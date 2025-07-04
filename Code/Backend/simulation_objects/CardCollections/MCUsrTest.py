from numpy import random
from simulation_objects.CardCollections.MonteCarlo import MonteCarlo


class MCUsrTest(MonteCarlo):
    def __init__(self, deck):
        MonteCarlo.__init__(self, deck)

    #run functions
    def output_cards(self) -> list[str]:
        return [
            "A list of lands!"
        ]

    def output_metrics(self):

        pain = self.min_sample(5.0, self.threshold)
        price = self.min_sample(98.70, self.budget)
        most_expensive = self.min_sample(10.03, self.mppc)
        basic_lands = self.minbasics + random.randint(4)
        misc = "Some other metrics! What might you want to see?"

        output = {
            "pain": pain,
            "price": price,
            "most_expensive": most_expensive,
            "basic_lands": basic_lands,
            "misc": misc
        }

        return output

    #functions that are not in the ancestor class


    def min_sample(self, arbitrary, input):
        m = int(min(arbitrary, input))
        output = random.randint(m)
        return output



