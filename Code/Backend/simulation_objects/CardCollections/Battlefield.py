import itertools
import pickle
import time
from itertools import product, combinations
from collections import Counter


from .CardCollection import CardCollection
from simulation_objects.GameCards import Land
from simulation_objects.Misc.Wodge import Wodge
from ..GameCards.RampLands.RampLand import RampLand
from simulation_objects.Misc.LandPermutationCache import LandPermutationCache
from ..GameCards.SearchLands import SearchLand


#global(big_ones) = 0

class Battlefield(CardCollection):
    def __init__(self, cache):
        CardCollection.__init__(self)
        self._permutations = []
        self._perms_as_dicts = []
        self._monomoots = []
        self._searchmoots = []
        #print(f"Set permutations as: {self._permutations}")
        #start = time.time()
        self._cache = cache
        #end = time.time()
        #total = (end - start) * 10000
        #print(f"Total: {total}")
        self._new_tapland = False

        #dev attributes
        self.altpermutations = []
        self.dummy_cache = {}

    #getters and setters
    @property
    def searchmoots(self):
        return self._searchmoots
    @searchmoots.setter
    def searchmoots(self, value):
        self._searchmoots = value

    @property
    def monomoots(self):
        return self._monomoots
    @monomoots.setter
    def monomoots(self, monomoots):
        self._monomoots = monomoots

    @property
    def new_tapland(self):
        return self._new_tapland
    @new_tapland.setter
    def new_tapland(self, value):
        self._new_tapland = value

    @property
    def cache(self):
        return self._cache

    @property
    def permutations(self) -> list:
        return self._permutations
    @permutations.setter
    def permutations(self, value):
        self._permutations = value

    @property
    def perms_as_dicts(self) -> list:
        return self._perms_as_dicts
    @perms_as_dicts.setter
    def perms_as_dicts(self, value):
        self._perms_as_dicts = value




    #pseudogetters
    def accessible_mana(self) -> list[Land]:
        return [l for l in self.card_list if not l.tapped and isinstance(l, Land)]

    def max_mana(self) -> int:
        output = 0
        for card in self.card_list:
            output += card.produced_quantity()
        return output
        #return [card.produced_quantity for card in self.card_list]
        #return len(self.accessible_mana())

    def filters(self) -> list:
        return [x for x in self.card_list if isinstance(x, RampLand)]

    #game actions
    def untap(self, game):
        for card in self._cards:
            card.tapped = False
        if self.new_tapland:
            self.new_tapland = False
            self.reset_permutations(game)


    #game information
    def determine_permutations(self, all_produced):
        all_combinations = product(*all_produced)
        return list(all_combinations)

    def determine_multicolor_permutations(self, multicolor_lands:Counter):
        """
        for each bundle of options, go through and identify if they are the product of, say, a dimir land
        So then enter into the function something like "dimir", "Simic", "sultai"
        the memoized function outputs a list of dicts, where each one is a permutation, something like dimir1: U, dimir2: B, Sultai1:G
        then assign these to your lands.


        OR:
        Each land gets something like "dual" vs "tri" vs "filter" vs "ramp" and then its colours.
        So back in the reset permutations function, go through each land and this function accepts stuff like dual UW, tri BUG, etc. It can accept them in any order.
        it then outputs a list of dicts, each of which is a permutation: Dual_UW: W, Tri_BUG: B, etc
        Then go throught these with your nonbasic lands and consult.

        How does the function itself actually work?



        """


    def handle_costed(self, combos):
        #as programmed this returns nothing, it only messes about in the lac
        pass

    def reset_permutations(self, game, extra_land=None):
        self.reset_permutations_v2(game, extra_land)
        """



        if game.prototype_comparison is None:
            self.reset_permutations_v1(game, extra_land)
            print("One!")
        else:
            self.reset_permutations_v2(game, extra_land)
            print("Two!")"""


        """ 
        self.reset_permutations_v2(game, extra_land)
        for item in self.permutations:
            for altitem in self.altpermutations:
                litem = len(item)
                laltitem = len(altitem) + len(self.monomoots)
                if litem != laltitem:
                    print(f"{item} ({litem})")
                    print(f"{altitem} {self.monomoots} ({laltitem})")
                    raise Exception("Halt!")
        """



    def reset_permutations_v1(self, game, extra_land=None):
        #self.reset_permutations_v2(game, extra_land)
        #starttime = time.time()
        game.vprint("Resetting permutations...")
        #all_info = [{"land": x, "produced":x.conditions(game)} for x in self.accessible_mana()]
        mana = self.accessible_mana()
        #print(f"Accessible: {self.accessible_mana()}; {self.accessible_mana()[0].enters_untapped(game)}")
        if extra_land != None and extra_land.enters_untapped(game):
            mana.append(extra_land)
        all_produced = [x.conditions(game) for x in mana]
        #lac = self.determine_permutations(all_produced)
        #print(f"{[len(x) for x in all_produced]}")
        all_combinations = product(*all_produced)
        lac = list(all_combinations)
        #if len(self.filters()) > 0:
            #self.handle_costed(lac)
        self.permutations = lac
        #print(self.permutations)
        #self.perms_as_dicts = self.perms_to_dicts(lac)
        #print(f"Created {len(self.permutations)} permutations out of {mana}")
        #self.reset_permutations_v2(game, extra_land=extra_land)
        #endtime = time.time()
        #print(endtime - starttime)
        
        


        #return list(all_combinations)

    def reset_permutations_v2(self, game, extra_land=None):
        #start = time.time()
        #game.vprint("Resetting permutations...")
        # all_info = [{"land": x, "produced":x.conditions(game)} for x in self.accessible_mana()]
        available = self.accessible_mana()
        if extra_land != None and extra_land.enters_untapped(game):
            available.append(extra_land)
        divided = self.divide_monos_and_multis(available)
        #multimoots = self.get_multicolor_permutations(divided["multi"], divided["mono"], game)
        othermoots = self.get_multicolor_permutations_v2(divided["multi"], divided["mono"], divided["search"], game)
        #print(f"Othermoots: {len(othermoots)}")
        #print(self.lands_list())
        #for m in othermoots:
            #print(f"\t{m}")
        #print("")
        self.permutations = othermoots["multis"]
        self.monomoots = othermoots["monos"]
        self.searchmoots = othermoots["search"]

        """        
        end = time.time()
        runtime = (end - start) * 90000
        print(runtime)
        
        if not self.hit:
            print("Miss")
        if runtime > 2000:
            print(f"{runtime} ({self.hit}) for {self.permlen} permutations")
            print(f"{self.lands_list()}")
            print("")"""


        """
        #cut out when you do this properly
        self.megaaltpermutations = []
        self.theothermoots = []
        for moot in multimoots:
            self.megaaltpermutations.append(tuple(moot))

        for moot in othermoots:
            self.theothermoots.append(tuple(moot))
        #print(f"{len(self.megaaltpermutations)} {len(self.permutations)} {len(othermoots)} {[f"{x} ({x.tapped})" for x in self.lands_list()]}")


        if self.permutations == self.theothermoots or len(self.permutations) < 4:
            print("Fine")
        else:
            print(f"Battlefield: {self.lands_list()}")
            print("Moots")
            for m in self.permutations:
                print(f"\t{m}")
            print("AltMoots")
            for m in self.megaaltpermutations:
                print(f"\t{m}")
            print("Othermoots")
            for m in self.theothermoots:
                print(f"\t{m}")
            raise Exception("Stop!")
        """

    def get_multicolor_permutations(self, lands:list[Land], monos:list[Land], game):
        live_prods = [x.conditions(game) for x in lands]
        mono_prods = [x.conditions(game)[0] for x in monos]

        lengths = [len(x) for x in live_prods]
        key = frozenset(Counter(lengths).items())

        abstract_permutations = self.recall_abstract_permutations(key, lengths)
        return self.determine_concrete_permutations(abstract_permutations, live_prods, mono_prods)



    def determine_concrete_permutations(self, abstract, prods, mono_prods):
        output = []
        for perm in abstract:
            concrete = []
            for letter, prod in zip(perm, prods):
                idx = ord(letter) - ord('A')
                concrete.append(prod[idx])
                #color = prod[idx]
                #concrete.append({'land': land, 'color': color})
            output.append(concrete)
            concrete.extend(mono_prods)
        return output

    def determine_named_permutations(self, abstract, multiprods, monoprods):
        concrete_permutations = []
        for perm in abstract:
            concrete = []
            for color, land in zip(perm, multiprods):
                concrete.extend([x for x in land if x["color"] == color])
                # Build your dict: which land produced which color
                #concrete.append({'land': land, 'color': color})
            concrete.extend(monoprods)
            concrete_permutations.append(concrete)

        return concrete_permutations




    def recall_abstract_permutations(self, key, lengths):
        if key in self.dummy_cache:
            return self.dummy_cache[key]
        else:
            sets = []
            for x in lengths:
                sets.append([chr(ord('A')+i) for i in range(x)])
            permutations = list(product(*sets))
            #try this out, see how far it goes
            #permutations = self.purge_permutations(unpurged)
            self.dummy_cache[key] = permutations
            return permutations

    def recall_permutations(self, key, lands, game):
        #print(key)
        if result := self.cache.get(key):
            #print("Cache hit!")
            #self.hit = True
            return result
        else:
            #self.hit = False
            print("Cache miss!")

            #print(f"{key} not in dummy_cache")
            groups = [land.live_prod(game) for land in lands]
            abstract_permutations = list(product(*groups))
            purged = self.purge_permutations(abstract_permutations)
            #purged = abstract_permutations
            #print(f"Purged: {purged}")
            self.cache.set(key, purged)
            self.cache.save()
            return purged


    def get_multicolor_permutations_v2(self, lands:list[Land], monos:list[Land], search:list[Land], game):
        key = self.canonicalize(lands, game)
        if len(search) > 1:
            raise Exception("hey, you shouldn't have multiple searchlands!")

        #multiprods = [x.conditions(game) for x in lands]
        monoprods = [x.conditions(game)[0]["color"] for x in monos]
        if len(search) == 1:
            searchprods = search[0].conditions(game)
        else:
            searchprods = ()


        return {
            "multis": self.recall_permutations(key, lands, game),
            "monos": monoprods,
            "search": searchprods
        }
        #self.abs = abstract_permutations
        #self.permlen = len(abstract_permutations)
        #for moot in abstract_permutations:
            #print(f"\t{moot}")
        #print(f"Abs: {abstract_permutations} lands: {self.lands_list()}")


    def purge_permutations(self, perms):
        seen = set()
        unique = []
        for p in perms:
            key = tuple(sorted(p))
            if key not in seen:
                seen.add(key)
                unique.append(p)
        #if len(perms) > 100:
            #print(f"Purged {len(perms) - len(unique)} of {len(perms)} permutations")
        return unique



    def canonicalize(self, lands:list[Land], game):
        frozen = [frozenset(land.live_prod(game)) for land in lands]
        return frozenset(Counter(frozen).items())

    def abstract_canonicalize(self, prods:dict) -> dict:
        as_numbers = [len(x) for x in prods]
        return {
            "key": frozenset(Counter(as_numbers).items()),
            "lengths": as_numbers}


    def add_land_to_permutations(self, game, land):
        #outputs list of list of dicts; note the original gave you list of tuples of dicts
        produced = land.conditions(game)
        if 3 == 1: #len produced equals 1
            for perm in self.altpermutations:
                perm.append(produced[0])
        else:
            perms = self.altpermutations
            new_perms = []
            if(len(perms) > 100):
                #global(big_ones) += 1
                print(f"Big one! {len(perms)}")
            for color in produced:
                for perm in perms:
                    tmp = [x for x in perm]
                    tmp.append(color)
                    new_perms.append(tuple(tmp))
            self.altpermutations = new_perms
        #print(f"Turn: {game.turn} Perms: {len(self.permutations)}; alts: {len(self.altpermutations)} ({self.lands_list()}")

        if(len(self.altpermutations) != len(self.permutations)) and len(self.lands_list()) > 4:
            print(f"Battlefield:{self.lands_list()}, accessible: {self.accessible_mana()}")
            print("Perms:")
            for perm in self.permutations:
                print(f"\t{perm}")
            print("Alts")
            for perm in self.altpermutations:
                print(f"\t{perm}")
            raise Exception("Different lengths")
        

        #print(self.altpermutations)




    def divide_monos_and_multis(self, cardlist) -> dict[str, list[Land]]:
        output = {
            "mono": [],
            "multi": [],
            "search": []
        }

        for card in cardlist:
            if isinstance(card, Land):
                if isinstance(card, SearchLand):
                    output["search"].append(card)
                if card.monocolor:
                    output["mono"].append(card)
                else:
                    output["multi"].append(card)
        #print(f"Lengths: {len(output["mono"])} {len(output['multi'])}")
        return output





    def encode_lump(self, game, lump):

        """
        if n is None:
            accessible = [(self.accessible_mana())]
        else:
            accessible = list(itertools.combinations(self.accessible_mana(), n))

            """

        lands = self.accessible_mana()

        accessible = list(itertools.combinations(lands, len(lands)))


        for bunch in accessible:
            #assert(len(bunch) == lump.cmc)
            lump.parse_wodge(Wodge(bunch, game))

        """
        metaout = []
        for arrangement in accessible:
            landinfo = []
            for land in arrangement:
                d = {
                    "land":land,
                    "produced": land.conditions(game)
                }
                landinfo.append(d)
                grouped = [land["produced"] for land in landinfo]
            combinations = product(*grouped)
            output = []

            for c in combinations:
                colours = [x["color"] for x in c]
                output.append(c)
            metaout.append(output)
        return metaout

        """

    def perms_to_dicts(self, input:list):
        output = []
        for option in input:
            colors = [x['color'] for x in option]
            dict = {'W':0, 'U':0, 'B':0, 'R':0, 'G':0, 'C':0}
            for color in colors:
                dict[color] += 1
            output.append(dict)
        return output










