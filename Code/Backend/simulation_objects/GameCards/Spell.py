from simulation_objects.GameCards.GameCard import GameCard
from database_management.models.Card import Card

class Spell(GameCard):
    def __init__(self, orm_obj:Card, mandatory=False, commander=False):
        GameCard.__init__(self, orm_obj, mandatory)
        self._mana = self.parse_mana(orm_obj)
        self._cmc = self.parse_cmc(self._mana)
        self._pips = self.parse_pips(self._mana)
        self._commander = commander

    #setters and getters
    @property
    def mana(self) -> list[dict[str, int]]:
        return self._mana

    @property
    def commander(self) -> bool:
        return self._commander

    @property
    def cmc(self) -> list[int]:
        return self._cmc

    @property
    def pips(self) -> list[dict[str, int]]:
        return self._pips



    #setup functions
    def parse_cmc(self, input:list[dict[str, int]]) -> list[int]:
        output = []
        for face in input:
            wubrg = [x for x in face.keys() if x != "X"]
            cost = 0
            for w in wubrg:
                cost += face[w]
            output.append(cost)
        return output

    def parse_mana(self, orm_obj:Card):
        output = []
        playable = [x for x in orm_obj.faces if x.playable]
        for face in playable:
            cost = list(face.mana_cost)
            d = {"W":0, "U":0, "B":0, "R":0, "G":0, "C":0, "X":0, "Gen":0}
            i = 0
            j = 1
            while i < len(cost):
                if cost[i] == "{":
                    pip = cost[j]
                    if str.isdigit(pip):
                        d["Gen"] += int(pip)
                    else:
                        d[pip] += 1
                i += 1
                j += 1
            output.append(d)
        return output

    def parse_pips(self, input):

        return {colour: quantity for colour, quantity in input[0].items() if colour not in {"X", "Gen"}}





    """    def parse_mana_cost(self, cost):
        self.generic = 0
        cost = list(cost)
        dict = {'W': 0, 'U': 0, 'B': 0, 'R': 0, 'G': 0, 'C': 0, 'X': 0, 'S': 0, 'Y': 0, 'Z':0}
        i = 0
        j = 1
        while i < len(cost):
            if cost[i] == "{":
                pip = cost[j]
                if str.isdigit(pip):
                    self.generic = int(pip)
                else:
                    dict[pip] += 1
            i += 1
            j += 1

        self.white = dict['W']
        self.blue = dict['U']
        self.black = dict['B']
        self.red = dict['R']
        self.green = dict['G']
        self.colorless = dict['C']
        self.x_in_cost = dict['X']
        self.snow = dict['S']"""

