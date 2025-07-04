from ..GameCards import Land
from itertools import combinations, product


class Wodge():
    def __init__(self, lands:list[Land], game):
        self._game = game
        self._lands = lands
        self._options = self.parse_options(lands)
        #for o in self._options:
            #print(f"Option length at init: {len(self._options[o])}")

    #getters and setters
    @property
    def game(self):
        return self._game

    @property
    def options(self):
        return self._options

    #setup functions
    def parse_options(self, input:list[Land]):
        landinfo = []
        for land in input:
            d = {
                "land":land,
                "produced": land.conditions(self.game)
            }
            landinfo.append(d)
        grouped = [land["produced"] for land in landinfo]
        combinations = product(*grouped)

        output = {}
        i = 1
        for c in combinations:
            #colors = [choice["color"] for choice in c]
            #print(f"Combination: {len(c)}")
            output[i] = c
            i += 1


        return output

