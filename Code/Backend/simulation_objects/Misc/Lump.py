import random
from copy import deepcopy
import time

from joblib import Parallel, delayed
from line_profiler import profile

from .ColorPie import piepips
from simulation_objects.GameCards.Spell import Spell
from simulation_objects.GameCards.BasicLand import BasicLand
from simulation_objects.Misc.WodgeSocket import WodgeSocket
from .Moot import Moot

import numpy as np
import scipy.optimize

from ..GameCards.PermaUntapped.FilterLand import FilterLand
from ..GameCards.RampLands.RampLand import RampLand

from itertools import permutations


def compute_prices(land, mana_required, game):
    return [land.set_price(game, m) for m in mana_required]

class Lump:
    def __init__(self, casting_list: {Spell:int}, **kwargs):

        self._to_cast = list(casting_list.keys())
        if 'landcount' in kwargs:
            self._mana_as_list = self.parse_cost_as_list(casting_list, self._to_cast, kwargs.get('landcount'))
        else:
            self._mana_as_list = None
        self._cost = self.parse_cost(casting_list, self._to_cast)
        self._cmc = self.parse_cmc(self._cost)
        #self._x = self._cost["X"] != 0 Temporarily disregarding X spels
        self._x = False
        self._pips = self.parse_pips_as_list(self._cost)
        self._colorpips = [x for x in self._pips if x not in ["Gen", "X"]]
        self._commander = len([x for x in self._to_cast if x.commander]) > 0

        #version 2
        self._playable = False
        self._mapping = {}

        self._colorless = self.parse_colorless(self._cost)
        self._wodges = []
        self._playmakers = []
        self._castable = False
        self._castable_with_generic = False
        self._moots = []
        self._originals = {"cmc": self._cmc, "cost": self._cost}
        self._searchland_present = False

        #dev attributes
        self.filterloops = 0
        self.starttime = 0


    def __repr__(self):
        return str(self._to_cast)

    @property
    def mana_as_list(self):
        return self._mana_as_list

    @property
    def commander(self):
        return self._commander

    @property
    def playable(self):
        return self._playable
    @playable.setter
    def playable(self, value):
        self._playable = value

    @property
    def mapping(self):
        return self._mapping
    @mapping.setter
    def mapping(self, value):
        self._mapping = value

    @property
    def pips(self):
        return self._pips

    @property
    def colorpips(self):
        return self._colorpips

    @property
    def searchland_present(self):
        return self._searchland_present
    @searchland_present.setter
    def searchland_present(self, value):
        self._searchland_present = value

    @property
    def originals(self):
        return self._originals
    @originals.setter
    def originals(self, value):
        self._originals = value

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
    @cmc.setter
    def cmc(self, value:bool):
        self._cmc = value


    @property
    def to_cast(self):
        return self._to_cast

    @property
    def wodges(self):
        return self._wodges

    @property
    def cost(self):
        return self._cost
    @cost.setter
    def cost(self, value):
        self._cost = value

    @property
    def colorless(self) -> bool:
        return self._colorless

    @property
    def castable_with_generic(self) -> bool:
        return self._castable_with_generic
    @castable_with_generic.setter
    def castable_with_generic(self, value:bool):
        self._castable_with_generic = value


    #VERSION 2
    #@profile
    def set_playability(self, lands, game, filter_subversion = False):
        #playstart = time.time()
        if not filter_subversion:
            if self.cmc > len(lands):
                return False
            if len(lands) == 0 and self.cmc == 0:
                return True

            self.account_for_ramplands(lands)

        invalid = 9999
        mana_required = self.mana_as_list
        #weightstart = time.time()
        #weighted = np.array([[land.set_price(game, m) for m in mana_required] for land in lands])
        weighted = [[land.set_price(game, m) for m in mana_required] for land in lands]
        #for item in weighted:
            #print(item)
        #print("")


        #weightrun = time.time() - weightstart
        #if weightrun > 0.001:
            #print(f"assigning weight took {weightrun} seconds for lands {lands}")
        row, col = scipy.optimize.linear_sum_assignment(weighted)
        cost = sum([weighted[row[i]][col[i]] for i in range(len(lands))])
        self.mapping = {}
        output = cost < invalid

        if output:
            for i in range(len(lands)):
                self.mapping[lands[row[i]]] = mana_required[col[i]]
        if not output:
            if not filter_subversion:
                if game.battlefield.filterlands_present():
                    return self.account_for_filterlands(lands, game)
        return output

    def cointoss(self):
        x = random.randint(1, 4)
        return x > 1

    def write_report(self, target, lands, message):
        for land in lands:
            if land.name == target:
                land.report(message)
                break


    def account_for_filterlands(self, lands, game):
        #print(f"\tAccounting for filterlands for {self} ({lands})")
        #print("Hey you're still accessing me somewhere ")
        if not self.check_filterland_feasible(lands):
            return False

        divided = self.divide_filters(lands)
        normals = divided["normals"]
        filters = divided["filters"]

        #filter_ids = tuple(sorted(f.id for f in filters))
        #filterperms = self.get_filter_permutations(filters)
        #filterperms = permutations(filters)

        start_combotime = time.time()
        for perm in permutations(filters):
            combinations = self.assign_filter_combinations_v2(perm, normals, game)
            #if len(filters) == 3:
                #print(f"Took {assigntime} seconds to get all {len(combinations)} combinations for permutation {perm}")
            for combination in combinations:
                self.filterloops += 1
                if self.set_playability(combination, game, filter_subversion = True):
                    #end_combotime = time.time() - start_combotime
                    #self.filter_report(game, True, time.time() - filterstart)
                    return True

        #end_combotime = time.time() - start_combotime
        #self.filter_report(game, False, time.time() - filterstart)
        return False

    def filter_report(self, game, success, runtime):
        if self.filterloops > 20:
            print(f"Took {runtime} to return a value of {success} over {self.filterloops} iterations for {self} with battlefield {game.battlefield.lands_list()}")

    def assess_filter_combinations(self, combos, game):

        pass

    def assign_filter_combinations(self, filters, normals, game):
        ncopy = [[x for x in normals]]
        for filter in filters:
            ncopy = self.get_filter_possibilties(filter, ncopy, game)
        yield from ncopy

    def assign_filter_combinations_v2(self, filters, normals, game):
        """
        Lazily yields all possible land configurations resulting from resolving the filters in order,
        replacing activating lands with sublands, and adding colorless-only if not activated.
        """

        def _recurse(filters_left, current_lands):
            if not filters_left:
                # No more filters to resolve; yield this land setup
                yield current_lands
                return

            current_filter = filters_left[0]
            remaining_filters = filters_left[1:]

            # Try all possible activating lands
            activated = False
            for i, land in enumerate(current_lands):
                if land.produces_at_least_one(current_filter.required, game):
                    # Replace this land with the filter's sublands
                    new_lands = current_lands[:i] + current_lands[i + 1:] + current_filter.sublands
                    yield from _recurse(remaining_filters, new_lands)
                    activated = True

            # If no land can activate this filter, add it as-is (colorless-only producer)
            if not activated:
                yield from _recurse(remaining_filters, current_lands + [current_filter])

        yield from _recurse(filters, normals)

    def get_filter_possibilties(self, filter, meta_normals, game):
        output = []
        #tmp = deepcopy(meta_normals)
        production_map = {}


        for sublist in meta_normals:
            #for land in sublist:
                #if isinstance(land, SubLand):
                    #print(f"Sublist: {sublist}")
            candidates = [x for x in sublist if x.produces_at_least_one(filter.required, game)]
            for candidate in candidates:
                permutation = [x for x in sublist if x != candidate]
                permutation.extend(filter.sublands)
                output.append(permutation)
            #sublist.append(filter)
            #output.append(sublist)
            output.append(sublist + [filter])
        #print(f"\t\tFor {filter} and meta normals: {tmp}, output is {output}")
        return output




    #lru_cache(maxsize=None)
    def get_filter_permutations(self, filters):
        return permutations(filters)

    def divide_filters(self, lands) -> dict:
        filters = []
        normals = []
        for land in lands:
            if isinstance(land, FilterLand):
                filters.append(land)
            else:
                normals.append(land)
        return {"normals": normals, "filters": filters}

    def check_filterland_feasible(self, lands) -> bool:
        return True

    def account_for_ramplands(self, lands):
        doppelgangers = []
        for land in lands:
            if isinstance(land, RampLand):
                doppelgangers.append(land)
        lands.extend(doppelgangers)

    def mana_as_list_live(self, length):
            output = []
            for item in self.cost:
                for _ in range(self.cost[item]):
                    if item not in ["W", "U", "B", "R", "G", "Gen"]:
                        print(f"Mana as list attempting to get {item}")
                    output.append(item)
            while len(output) < length:
                output.append("None")
            return output


    def tap_mana_v2(self, game):
        for key in self.mapping:
            key.tap_for_v2(self.mapping[key], game)







    def parse_pips_as_list(self, cost):
        output = []
        for initial in cost:
            for _ in range(cost[initial]):
                output.append(initial)
        return output




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
        if isinstance(sub, dict):
            if isinstance(sub["color"], str):
                return [sub["color"]]
            return sub["color"]
        elif isinstance(sub, str):
            return [sub]
        elif isinstance(sub, list):
            return sub
        else:
            raise Exception("Attempting to parse an invalid submission option")

    def check_pip_castability(self, option, crack=None) -> list[str]:
        colors = []
        for item in option:
            colors.extend(self.parse_submission_color(item))
            if crack is not None:
                colors.extend(crack)
        #print(f"colors: {colors}")
        one_offs = []
        castable = True
        missing = []
        for initial in piepips:
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
        for pip in piepips:
            if input[pip] != 0:
                return False
        return True

    def parse_cost_as_list(self, input, keys, excess):
        output = []
        for key in keys:
            spell_cost = key.mana[input[key]]
            for spell_key in list(spell_cost.keys()):
                for _ in range(spell_cost[spell_key]):
                    if spell_key == "X":
                        output.append("Gen")
                    else:
                        output.append(spell_key)
        while len(output) < excess:
            output.append("None")
        return output

    def parse_cost(self, input, keys):
        #output = {"W":0, "U":0, "B":0, "R":0, "G":0, "C":0, "X":0, "Gen":0} #doing a version without X
        output = {"W":0, "U":0, "B":0, "R":0, "G":0, "C":0, "Gen":0}
        wubrg = list(output.keys())
        for key in keys:
            cost = key.mana[input[key]]
            for color in wubrg:
                output[color] += cost[color]
        return output


    def parse_moots(self, input:list, monoprods = [], search = ()):
        self.tribute = False

        if len(self.to_cast) == 1 and self.to_cast[0].name == "Tribute to the World Tree":
            self.tribute = True
            #print(f"Cost: {self.cost}")


        if monoprods != []:
            self.subtract_monoprods(monoprods) #GET IT TO RESTORE ORIGINAL CMC/PIPS
        if search != ():
            self.searchland_present = True


        self.castable = False
        self.moots = []

        if input == []:
            self.empty_moot()
        else:
            if len(search) == 0:
                self.full_moot(input)
            else:
                for color in search:
                    self.full_moot(input, crack=color)

        self.reset_original_values()

    def reset_original_values(self):
        self.cmc = self.originals["cmc"]
        self.cost = self.originals["cost"]
        assert(self.tribute == False or self.cost["G"] == 3)
            #self.tprint(f"Reset to {self.cost} using {self.originals["cost"]}")

    def tprint(self, text):
        if self.tribute:
            print(text)

    def subtract_monoprods(self, prods):
        self.originals = {"cmc": self.cmc,
                          "cost": deepcopy(self.cost)}
        #oldcmc = self.cmc
        #oldcost = self.cost

        for letter in prods:
            if self.cost[letter] > 0:
                self.cost[letter] -= 1
                self.cmc -= 1
            elif self.cost['Gen'] > 0:
                self.cost['Gen'] -= 1
                self.cmc -= 1
        """
        print(f"Monoprods: {prods}")
        for letter in prods:
            self.cmc -= 1
            if self.cost[letter] > 0:
                self.cost[letter] -= 1
        print(f"Cost: {self.cost} Cmc: {self.cmc}")"""




    def empty_moot(self):
        initials = ["W", "U", "B", "R", "G", "C"]
        tmppips = []
        for initial in initials:
            for _ in range(0, self.cost[initial]):
                tmppips.append(initial)

        #print(f"tmppips: {tmppips}, gen: {self.cost['Gen']}")

        creation = Moot(None, tmppips, self.cost["Gen"])

        self.moots.append(creation)


    def full_moot(self, input:list, crack=None):

        generic_moot = False

        for option in input:
            pips = self.check_pip_castability(option, crack=crack)
            option_cmc = self.get_option_cmc(option, crack=crack)
            generic = max(0, self.cmc - option_cmc - len(pips))
            new_moot = Moot(option, pips, generic, crack=crack)
            if new_moot.castable:
                self.castable = True
                if new_moot.includes_searchland:
                    new_moot.generalize_searchland(self)
                #assert(self.cmc <= len(option))
                #print(f"cmc{self.cmc}, optionlen = {len(option)}")
            if len(new_moot.pips) == 0:
                generic_moot = True
            self.moots.append(new_moot)
            if self.castable:
                break
            #self.moots.append(Moot(option, pips, generic))

        self.cull_moots(generic_moot)


    def get_option_cmc(self, option, crack=None):
        output = 0
        for item in option:
            output += len(self.parse_submission_color(item))
        if crack is None:
            return output
        else:
            return output + 1






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
        if self.searchland_present:
            crackmoots = [m for m in self.moots if m.castable and m.crack != None]
            anycrackmoots = [m for m in crackmoots if m.crack["color"] == "Any"]
            if len(anycrackmoots) > 0:
                anycrackmoots[0].crack_fetch(game)
            elif len(crackmoots) > 0:
                crackmoots[0].crack_fetch(game)
        """
        for m in self.moots:
            if m.castable:
                m.tap_moot_mana(game)
                self.assess_land_contributions(m)
                break"""


    def prioritize_agnostic_moot(self, game):
        finished = False
        for m in self.moots:
            if m.searchland_agnostic(self, game):
                m.tap_moot_mana(game)
                finished = True
                self.assess_land_contributions(m)
                break
        if finished == False:
            self.play_first_moot()



    def play_first_moot(self, game):
        for m in self.moots:
            if m.castable:
                m.tap_moot_mana(game)
                self.assess_land_contributions(m)
                break


    def prioritize_moots(self, game) -> list[Moot]:
        #arranges your moots to make sure you're using your fetchlands responsibly
        #if not game.battlefield.contains_searchland():
        #maybe instead of searching the battlefield for fetchlands you should make "crack a fetch" an optional parameter, default false, in tap_mana?
        return self.moots





    def assess_land_contributions(self, m):
        #print(self.cost)
        #print(m.option)
        basics = []
        nonbasics = []
        for item in m.option:
            if isinstance(item['land'], BasicLand):
                basics.append(item['land'])
            else:
                nonbasics.append(item['land'])
        self.pay_mana(basics, m)
        self.pay_mana(nonbasics, m)

    def pay_mana(self, sources:list, moot):
        pass
        








