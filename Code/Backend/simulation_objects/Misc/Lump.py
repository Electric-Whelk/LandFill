from simulation_objects.GameCards.Spell import Spell
from simulation_objects.Misc.WodgeSocket import WodgeSocket

class Lump:
    def __init__(self, casting_list: {Spell:int}):
        self._to_cast = list(casting_list.keys())
        self._cost = self.parse_cost(casting_list, self._to_cast)
        self._cmc = self.parse_cmc(self._cost)
        self._x = self._cost["X"] != 0
        self._wodges = []

    def __repr__(self):
        return str(self._to_cast)

    @property
    def cmc(self):
        return self._cmc

    @property
    def to_cast(self):
        return self._to_cast

    @property
    def wodges(self):
        return self._wodges

    @property
    def cost(self):
        return self._cost


    def check_option_castability(self, option):
        colors = [x["color"] for x in option]
        one_offs = []
        castable = True
        cost = self.cost
        blacklisted = ["Gen", "X"]
        for initial in cost:
            if initial not in blacklisted:
                needed = cost[initial]
                available = colors.count(initial)
                if needed > available:
                    castable = False

                    if needed == available + 1:
                        one_offs.append(initial)

        if castable:
            return "castable"

        if len(one_offs) == 1:
            return one_offs[0]

        return "uncastable"



    def check_wodge_playability(self, wodge):
        pass





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

    def parse_wodge(self, wodge):
        castable = []
        uncastable = []
        options = wodge.options
        for index in wodge.options:
            #print(f"While iterating: {len(options[option])}")
            op = options[index]
            result = self.check_option_castability(op)
            match(result):
                case "castable":
                    castable.append(index)
                case "uncastable":
                    uncastable.append(index)
                case _:
                    uncastable.append(index)
            #print(f"{[x["color"] for x in op]}: {result}")

        self.wodges.append(WodgeSocket(wodge, castable, uncastable))





