from simulation_objects.GameCards.Spell import Spell

class Lump:
    def __init__(self, casting_list: {Spell:int}):
        self._to_cast = list(casting_list.keys())
        self._cost = self.parse_cost(casting_list, self._to_cast)
        self._cmc = self.parse_cmc(self._cost)
        self._x = self._cost["X"] != 0

    def __repr__(self):
        return str(self._to_cast)

    @property
    def cmc(self):
        return self._cmc

    @property
    def to_cast(self):
        return self._to_cast




    def parse_cmc(self, input:dict[str:int]) -> int:
        wubrg = [x for x in input.keys() if x != "X"]
        output = 0
        for w in wubrg:
            output += input[w]
        return output




    def parse_cost(self, input, keys):
        output = {"W":0, "U":0, "B":0, "R":0, "G":0, "C":0, "X":0, "Gen":0}
        wubrg = list(output.keys())
        for key in keys:
            cost = key.mana[input[key]]
            for color in wubrg:
                output[color] += cost[color]
        return output



