from .ColorPie import pips
from simulation_objects.GameCards.Spell import Spell
from simulation_objects.Misc.WodgeSocket import WodgeSocket
from .Moot import Moot


class Lump:
    def __init__(self, casting_list: {Spell:int}):
        self._to_cast = list(casting_list.keys())
        self._cost = self.parse_cost(casting_list, self._to_cast)
        self._cmc = self.parse_cmc(self._cost)
        self._x = self._cost["X"] != 0
        self._colorless = self.parse_colorless(self._cost)
        self._wodges = []
        self._playmakers = []
        self._castable = False
        self._castable_with_generic = False
        self._moots = []


    def __repr__(self):
        return str(self._to_cast)

    @property
    def moots(self):
        return self._moots
    @moots.setter
    def moots(self, moots):
        self._moots = moots

    @property
    def castable(self) -> bool:
        return self._castable
    @castable.setter
    def castable(self, value:bool):
        self._castable = value

    @property
    def playmakers(self) -> list[str]:
        return self._playmakers
    @playmakers.setter
    def playmakers(self, value:list[str]):
        self._playmakers = value

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

    @property
    def colorless(self) -> bool:
        return self._colorless

    @property
    def castable_with_generic(self) -> bool:
        return self._castable_with_generic
    @castable_with_generic.setter
    def castable_with_generic(self, value:bool):
        self._castable_with_generic = value

    def mana_to_seek(self):
        output = []
        if self.castable:
            #print(f"\t{self} can be cast")
            return output
        else:
            for m in self.moots:
                for p in m.pips:
                    if p not in output:
                        output.append(p)
        return output





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

    def parse_submission_color(self, sub):
        if isinstance(sub["color"], str):
            return [sub["color"]]
        return sub["color"]

    def check_pip_castability(self, option) -> list[str]:
        #if self.colorless:
            #return "castable"
        #colors = [*self.parse_submission_color(x) for x in option]
        colors = []
        for item in option:
            colors.extend(self.parse_submission_color(item))
        #print(f"colors: {colors}")
        one_offs = []
        castable = True
        missing = []
        for initial in pips:
            needed = self.cost[initial]
            available = colors.count(initial)
            diff = needed - available
            for _ in range(diff):
                missing.append(initial)
        return missing

    def check_playmaker(self, game, land) -> bool:
        if self.castable:
            return True

        colors_enough = False
        mana_enough = False

        prod = land.produced_on_entry(game)
        prod_colours = [o[("color")] for o in prod]
        #print(f"\tChecking as playmaker for {self}")
        for m in self.moots:
            #print(f"\t\tchecking {m}")
            if m.accept_submission(prod_colours):
                if m.accept_mana_submission(land, game):
                    return True
        return False









    def check_wodge_playability(self, wodge):
        pass




    def parse_cmc(self, input:dict[str:int]) -> int:
        wubrg = [x for x in input.keys() if x != "X"]
        output = 0
        for w in wubrg:
            output += input[w]
        return output

    def parse_colorless(self, input:dict) -> bool:
        for pip in pips:
            if input[pip] != 0:
                return False
        return True


    def parse_cost(self, input, keys):
        output = {"W":0, "U":0, "B":0, "R":0, "G":0, "C":0, "X":0, "Gen":0}
        wubrg = list(output.keys())
        for key in keys:
            cost = key.mana[input[key]]
            for color in wubrg:
                output[color] += cost[color]
        return output

    def parse_moots(self, input:list):
        self.castable = False
        self.moots = []

        if input == []:
            self.empty_moot()
        else:
            self.full_moot(input)

    def empty_moot(self):
        initials = ["W", "U", "B", "R", "G", "C"]
        tmppips = []
        for initial in initials:
            for _ in range(0, self.cost[initial]):
                tmppips.append(initial)

        #print(f"tmppips: {tmppips}, gen: {self.cost['Gen']}")

        creation = Moot(None, tmppips, self.cost["Gen"])

        self.moots.append(creation)


    def full_moot(self, input:list):

        generic_moot = False

        for option in input:
            pips = self.check_pip_castability(option)
            option_cmc = self.get_option_cmc(option)
            generic = max(0, self.cmc - option_cmc - len(pips))
            new_moot = Moot(option, pips, generic)
            if new_moot.castable:
                self.castable = True
                #assert(self.cmc <= len(option))
                #print(f"cmc{self.cmc}, optionlen = {len(option)}")
            if len(new_moot.pips) == 0:
                generic_moot = True
            self.moots.append(Moot(option, pips, generic))
        self.cull_moots(generic_moot)


    def get_option_cmc(self, option):
        output = len(option)
        output = 0
        for item in option:
            output += len(self.parse_submission_color(item))
        return output






        """
            assert(len(option) == self.cmc - 1)
            playmaker = self.check_pip_castability(option)
            if len(playmaker) == 0:
                self.castable_with_generic = True
                break
            else:
                self.playmakers.append(playmaker)
                      
        self.playmakers = []
        print(self)
        for option in input:
            print(f"\t{[x["color"] for x in option]} -> needs {self.check_option_castability_v2(option)}")

        pass
        """

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
                    self.playmakers.append(result)
            print(f"{[x["color"] for x in op]}: {result}")

        self.wodges.append(WodgeSocket(wodge, castable, uncastable))


    def cull_moots(self, generic:bool):
        if generic:
            for moot in self.moots:
                if len(moot.pips) != 0:
                    self.moots.remove(moot)


    def tap_mana(self, game):
        for m in self.moots:
            if m.castable:
                m.tap_moot_mana(game)
                break









