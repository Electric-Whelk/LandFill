import random
from copy import deepcopy

from itertools import combinations
from tabnanny import verbose

from simulation_objects.CardCollections.Battlefield import Battlefield
from simulation_objects.CardCollections.CardCollection import CardCollection
from simulation_objects.CardCollections.Deck import Deck
from simulation_objects.CardCollections.Graveyard import Graveyard
from simulation_objects.CardCollections.Hand import Hand
from simulation_objects.GameCards import PainLand, ShockLand, GameCard
from simulation_objects.GameCards.Land import Land
from simulation_objects.GameCards.SearchLands.FetchLand import FetchLand
from simulation_objects.GameCards.SearchLands.SearchLand import SearchLand
from simulation_objects.GameCards.Spell import Spell
from simulation_objects.GameCards.TappedCycles.Triome import Triome
from simulation_objects.Misc.Lump import Lump
from simulation_objects.Simulations.Simulation import Simulation
from simulation_objects.Timer import functimer_perturn


class Game(Simulation):
    def __init__(self, deck, cache, turns=7, verbose=False, prototype_comparison = None):
        Simulation.__init__(self, deck)
        self._hand = Hand()
        self._battlefield = Battlefield(cache)
        self._graveyard = Graveyard()
        self._turn = 0


        self._total_turns = turns


        #global reset during the turn
        self._lumps = []
        self._spell_lumps = []
        self._secondmain = False
        self._last_land_played = None

        #stats variables
        self._wasteless_turns = 0

        #variables that support the stats variables
        self._spent_this_turn = 0
        self._played_lands = []


        #dev attributes
        self.verbose = verbose #verbose
        self.log = []
        self.decisions = 0
        self.total_spent_mana = 0
        self.options_per_turn = 0
        self.total_played_lands = 0
        self.on_curve_casts = 0
        self.castable_cmc_in_hand = 0
        self.total_theoretcial_mana = 0
        self.leftover_mana = 0
        self.shockproblems = 0
        self.painproblems = 0
        self.fetchproblems = 0
        #self.played_lands = []

        self.prototype_comparison = prototype_comparison
        self.copydeck = None
        self.copyhand = None


    #getters
    @property
    def total_turns(self) -> int:
        return self._total_turns

    @property
    def played_lands(self):
        return self._played_lands
    @played_lands.setter
    def played_lands(self, value:list):
        self._played_lands = value

    @property
    def wasteless_turns(self) -> int:
        return self._wasteless_turns
    @wasteless_turns.setter
    def wasteless_turns(self, value:int):
        self._wasteless_turns = value

    @property
    def spent_this_turn(self) -> int:
        return self._spent_this_turn
    @spent_this_turn.setter
    def spent_this_turn(self, value:int):
        self._spent_this_turn = value

    @property
    def last_land_played(self) -> Land:
        return self._last_land_played
    @last_land_played.setter
    def last_land_played(self, land_played:Land) -> None:
        self._last_land_played = land_played

    @property
    def spell_lumps(self):
        return self._spell_lumps
    @spell_lumps.setter
    def spell_lumps(self, spell_lumps):
        self._spell_lumps = spell_lumps

    @property
    def secondmain(self):
        return self._secondmain
    @secondmain.setter
    def secondmain(self, value):
        self._secondmain = value

    @property
    def lumps(self):
        return self._lumps
    @lumps.setter
    def lumps(self, lumps):
        self._lumps = lumps


    @property
    def hand(self) -> Hand:
        return self._hand

    @property
    def battlefield(self) -> Battlefield:
        return self._battlefield

    @property
    def graveyard(self) -> Graveyard:
        return self._graveyard

    @property
    def turn(self) -> int:
        return self._turn
    @turn.setter
    def turn(self, turn):
        self._turn = turn

    #psuedogetters
    @property
    def max_mana(self) -> int:
        return self._turn

    @property
    def lands_in_hand(self) -> list:
        return [l for l in self.hand.card_list if isinstance(l, Land)]

    def absent_pips(self, exclude=None):
        req = self.required_pips()
        print(f"req: {req}")
        acc = self.accessible_pips(exclude=exclude)
        print(f"acc: {acc}")
        return self.subtract_pips(req, acc)


    def accessible_pips(self, exclude=None):
        hac = self.hand.accessible_colours(self, exclude=exclude)
        bac = self.battlefield.accessible_colours(self, exclude=exclude)
        return self.sum_pips(hac, bac)

    def required_pips(self):
        return self.hand.necessary_colours()

    #dev methods
    def vprint(self, input):
        if self.verbose:
            print(input)
        if self.log is not None:
            self.log.append(input)

    def oor(self, input):
        try:
            return input[0]
        except IndexError:
            return "NONE"

    def sample_hand(self, input:list, topdeck=[]):
        self.deck.shuffle()
        for term in input:
            self.deck.give(self.hand, self.tutor(term))
        for term in topdeck:
            card = self.tutor(term)
            self.deck.card_list.insert(0, card)

    def tutor(self, input:str) -> GameCard:
        for card in self.deck.card_list:
            if card.name == input:
                return card
        return None






    #run!
    def conclude_game(self):
        zones = [self.hand, self.battlefield, self.graveyard]
        self.options_per_turn /= self.total_turns
        #self.total_spent_mana /= self.total_played_lands #NOTE THAT THIS INCLUDES FETCHED LANDS
        #self.total_spent_mana /= self.castable_cmc_in_hand
        self.leftover_mana = self.total_theoretcial_mana - self.total_spent_mana
        if self.leftover_mana == 0:
            if self.wasteless_turns != self.total_turns:
                print(f"Uh oh!")



        for zone in zones:
            for item in zone.card_list:
                if isinstance(item, Land) and zone != self.hand: #you also need to set this to cover mandatory
                    item.award_points(self.leftover_mana, self.options_per_turn)
            zone.give_all(self.deck)

        self.vprint("Game complete")
        self.vprint(f"Leftover mana: {self.leftover_mana}\n")
        if self.prototype_comparison is not None:
            if self.leftover_mana == 0 or self.prototype_comparison["leftover_mana"] == 0:
                if self.leftover_mana != self.prototype_comparison["leftover_mana"]:
                    print("---------------ORIGINAL---------------")
                    for item in self.prototype_comparison["log"]:
                        print(item)
                    print("---------------PROTOTYPE---------------")
                    for item in self.log:
                        print(item)
                    raise Exception("Stop!")

    def run(self):
        #samplehand = ["Putrefy", "Lightning Greaves", "Misty Rainforest", "Island", "Mystic Remora", "Forest", "Llanowar Wastes"] #Misty Rainforest/Watery Grave
        #topdeck =  ["Phyrexian Arena","Verdant Catacombs", "Swamp", "Risen Reef"] #Verdat Catacombs/Breeding Pool
        #self.sample_hand(samplehand, topdeck=topdeck)

        if self.prototype_comparison == None:
            self.setup_game()
        else:
            self._hand = self.prototype_comparison["hand"]
        #self.setup_game()

        #samplehand = ["Forest", "Mycoloth", "Underground River", "Watchful Radstag", "Tribute to the World Tree", "Drowned Catacomb", "Zagoth Triome"]
        topdeck = ["Haunting Imitation", "Tender Wildguide","Propagator Drone","Glen Elendra Archmage", "Polluted Delta","Cyclonic Rift","Xavier Sal, Infested Captain"]
        #topdeck = ["Xavier Sal, Infested Captain", "Cyclonic Rift", "Polluted Delta", "Glen Elendra Archmage", "Propagator Drone", "Tender Wildguide", "Haunting Imitation"]
        #self.sample_hand(samplehand, topdeck=topdeck)
        for _ in range(self.total_turns): #SCAFFOLD - number of turns
            self.run_turn()

        self.conclude_game()
        self.turn = 0
        pass

    def play_land(self, land, library=False):
        if land is not None:
            if library:
                self.vprint(f"Fetching {land} from library")
                self.deck.give(self.battlefield, land)
            else:
                self.vprint(f"Playing {land}...")
                self.hand.give(self.battlefield, land)
            land.run_etb(self)
            land.tapped = not land.enters_untapped(self)
            self.last_land_played = land
            land.tapped = not land.enters_untapped(self)
            #land.peek_board_state(self)
            #if not isinstance(land, SearchLand):
            self.played_lands.append(land)
            self.battlefield.reset_permutations(self)
            """
            if isinstance(land, SearchLand) and len(self.hand.card_list) == 0 and self.total_spent_mana == self.total_theoretcial_mana:
                self.fetchproblems += 1
            elif isinstance(land, PainLand) and len(self.hand.card_list) == 0 and self.total_spent_mana == self.total_theoretcial_mana:
                self.painproblems += 1
            elif isinstance(land, ShockLand) and len(self.hand.card_list) == 0 and self.total_spent_mana == self.total_theoretcial_mana:
                self.shockproblems += 1#
                """
            #when gettinbg back into test mode, remember to turn permutations back to a list of tuples
                #self.battlefield.add_land_to_permutations(self, land)
            #self.battlefield.add_land_to_permutations(self, land)
            self.total_played_lands += 1
        else:
            self.vprint("No land to play")


    def play_land_at_random(self):
        lands = [l for l in self.hand.card_list if isinstance(l, Land)]
        if len(lands) > 0:
            self.hand.give(self.battlefield, lands[0])

    def play_lump(self, lump):
        try:
            lump.tap_mana(self)
            if lump.cmc > self.battlefield.max_mana():
                print(f"Uh oh - casting {lump} on a battlefield of {self.battlefield}")
            self.spent_this_turn = lump.cmc
            for spell in lump.to_cast:
                self.total_spent_mana += spell.cmc[0]
                self.vprint(f"Playing {spell} at cost {spell.cmc[0]}...")
                self.hand.give(self.battlefield, spell)
        except AttributeError as e:
            self.vprint("No playable lumps")


    def run_turn(self):
        self.spent_this_turn = 0
        self.turn += 1
        #if len([x for x in self.hand.lands_list() if isinstance(x, SearchLand)]) > 0:
            #self.verbose = True
        self.battlefield.untap(self)
        self.battlefield.reset_permutations(self)
        self.draw()
        self.vprint(f"Hand: {self.hand.card_list}")
        self.vprint(f"Battlefield: {self.battlefield.card_list} ")
        self.determine_play()
        #self.play_land_at_random()
        self.move_through_phases()
        #if len(self.hand.card_list) == 0:
            #raise Exception("Nada!")

    def move_through_phases(self):
        self.secondmain = True
        self.tap_unused_lands()
        self.reset_values()
        self.vprint("")

    def mulligan(self, times):
        if len(self.lands_in_hand) < 3:
            self.hand.give_all(self.deck)
            self.vprint(f"Mulliganing")
            #print(f"Mulliganing...{times}")
            return True
        #if self.prototype_comparison is None:
            #self.copydeck = deepcopy(self.deck)
            #self.copyhand = deepcopy(self.hand)
        return False


    def setup_game(self):
        deck = self.deck
        deck.shuffle()
        mull = True
        i = 0
        while mull: #and i < 2
            self.draw(7)#restricting to two mulls
            i += 1
            mull = self.mulligan(i)
        #if i == 2:
            #self.draw(7)
        #assert(len(self.lands_in_hand) != 0)

    def tap_unused_lands(self):
        for land in self.battlefield.lands_list():
            if not land.tapped:
                land.conclude_turn(self)


    #game actions
    def draw(self, repeats=1):
        for _ in range(repeats):
            self.deck.give_top(self.hand)


    #strategizing algorithms
    def hand_cant_produce(self, color, exclude=None):
        if exclude is None:
            l = len([x for x in self.hand.card_list if x.can_produce(color, self)])
        else:
            l = len([x for x in self.hand.card_list if x.can_produce(color, self) and x != exclude])
        return l == 0

    def prioritize_tapland(self, input:list[Land], library=False):
        #add a layer so that it prioritizes fetchlands that can get a perm over a current, and fetchlands that can get a current over a leftover
        perm = []
        current = []
        leftover = []
        for land in input:
            if land.permatap:
                perm.append(land)
            elif not land.enters_untapped(self):
                current.append(land)
            else:
                leftover.append(land)
        if len(perm) > 0:
            self.play_land(perm[0], library=library)
            #source.give(self.battlefield, perm[0])
        elif len(current) > 0:
            self.play_land(current[0], library=library)
            #source.give(self.battlefield, current[0])
        elif len(leftover) > 0:
            self.play_land(leftover[0], library=library)
            #source.give(self.battlefield, leftover[0])





    def reset_values(self):
        self.lumps = []
        self.spell_lumps = []
        self.secondmain = False


    def create_lumps(self, input:list[Spell]) -> list[Lump]:
        #draft version that picks a MDFC output randomly, but there is room to improve here by getting all MDFC permutations
        fodder = {}
        for spell in input:
            if len(spell.mana) == 1:
                fodder[spell] = 0
            else:
                fodder[spell] = random.randint(0, 1)
        return [Lump(fodder)]

    def determine_and_play_land(self, playoptions:dict):
        champ = None
        champlen = 0
        for option in playoptions:
            if champ == None:
                champ = option
                champlen = playoptions[option]
            elif playoptions[option] > playoptions[champ]:
                champ = option
                champlen = playoptions[option]
                self.decisions += 1


        allows_highest_expenditure = [land for land in playoptions if playoptions[land] >= champlen]
        provides_most_colours =  self.provides_most_colours(allows_highest_expenditure)


        self.prioritize_tapland(provides_most_colours)


    def determine_and_play_lump(self):
        new_moots = self.battlefield.permutations
        new_monos = self.battlefield.monomoots
        search = self.battlefield.searchmoots
        new_playable = []
        for lump in self.lumps:
            lump.parse_moots(new_moots, monoprods=new_monos, search=search)
            if lump.castable:
                new_playable.append(lump)
        self.options_per_turn += len(new_playable)

        lumpchamp = None
        for option in new_playable:
            if lumpchamp == None or option.cmc > lumpchamp.cmc:
                lumpchamp = option
        if lumpchamp != None and lumpchamp.cmc == self.battlefield.max_mana():
            self.on_curve_casts += 1

        self.play_lump(lumpchamp)


    def determine_spell_lumps(self, input:list[Spell]) -> list[Lump]:
        output = []
        for spell in input:
            new_lumps = self.create_lumps([spell])
            output.extend(new_lumps)
        return output

    def determine_lumps_from_hand(self, input:list[Spell]) -> list[Lump]:
        #m previously set as self.turn
        max = m = self.battlefield.max_mana() + 1
        minrange = min(m, 3) + 1

        #allowing some looking ahead if you have a fetchland
        #fetches_in_hand = [x for x in self.hand.card_list if isinstance(x, FetchLand)]
        #if len(fetches_in_hand) > 0:
           # max = m = len(self.hand.lands_list()) + len(self.battlefield.lands_list())
            #minrange = m + 1


        fodder = [x for x in input if x.cmc[0] <= max]
        output = []
        l = len(fodder)
        #print(f"found fodder: {fodder} with minrange {minrange}")
        #print(f"Max: {self.battlefield.max_mana()}")
        #l bpm = 66
        #self.battlefield.max_mana bpm = 109
        #never more than 3 = can no longer keep count
        #min(m, 3) + 1

        for r in range(1, minrange):
            #print(f"R: {r}")
            combos = combinations(fodder, r)
            #as_list = list(combos)
            #print(f"Combos returned {len(as_list)} combos for range {r}")
            for c in combos:
                summed = sum([x.cmc[0] for x in c])
                if summed <= max:
                    output.extend(self.create_lumps(c))

                """
                if self.prototype_comparison is None:
                    output.extend(self.create_lumps(c))
                else:
                    #print(f"c:{c} for max:{max}")
                    summed = sum([x.cmc[0] for x in c])
                    self.vprint(f"{c} summed to {summed} for max {max}")
                    #print(f"Summed: {summed}")
                    if summed <= max:
                        output.extend(self.create_lumps(c))"""

            #print("")

        #purged_output = self.purge_lumps(output)
        #print(f"{m}: purged {len(output)-len(purged_output)} from {len(output)} lumps ({input})")
        #return purged_output
        return output


    def determine_max_mana(self) -> int:
        return self.turn


    def determine_play(self):
        lands = [x for x in self.hand.card_list if isinstance(x, Land)]
        self.vprint(f"begnning turn {self.turn} with {lands} in hand and {self.battlefield.lands_list()} on battlefield {[x.live_prod(self) for x in self.battlefield.lands_list()]}")
        spells = self.hand.spells_list()
        lumps = self.determine_lumps_from_hand(spells)
        self.lumps = lumps
        self.spell_lumps = self.determine_spell_lumps(spells)
        self.vprint(f"identified {len(self.lumps)} lumps")
        #self.vprint(f"Playable cards: {fodder} divisible into {len(lumps)} lumps")

        moots = self.battlefield.permutations
        monomoots = self.battlefield.monomoots
        search = self.battlefield.searchmoots
        for lump in lumps:
            lump.parse_moots(moots, monoprods=monomoots, search=search)

        for lump in self.spell_lumps:
            lump.parse_moots(moots, monoprods=monomoots, search=search)

        castable = []
        not_castable = []


        for lump in lumps:
            if lump.castable:
                castable.append(lump)
            else:
                not_castable.append(lump)


        playoptions = {}

        self.vprint(f"The following {len(castable)} lumps are playable: {castable}")

        no_playmakers = True
        for land in lands:
            enabled = [l for l in lumps if l.check_playmaker(self, land)]
            playmaker_count = len(enabled)
            playoptions[land] = playmaker_count
            if playmaker_count > 0:
                no_playmakers = False
            self.vprint(f"Playing {land} will allow {playoptions[land]} lumps to be played ({enabled})")



        if no_playmakers:
            self.determine_and_play_lump()
            self.determine_and_play_land(playoptions)
            #if you might be playing a lump before sorting permutations, make sure to allow for lands that are untapped
            #this is a very brute force way to do it but w/e
            self.battlefield.new_tapland = True
        else:
            self.determine_and_play_land(playoptions)
            self.determine_and_play_lump()

        """
        Number of turns we had enough lands to cast at least one of the lump in our hand
        Regadless of whether it's the right spell
        """

        self.assess_turn_score()


    def assess_turn_score(self):
        maxmana = self.battlefield.max_mana()
        achievable = [lump for lump in self.lumps if lump.cmc <= maxmana]
        try:
            largest_achievable = max(lump.cmc for lump in achievable)
            self.vprint(f"largest: {largest_achievable}")
        except ValueError:
            largest_achievable = 0
        self.total_theoretcial_mana += largest_achievable
        wasteless = False
        if largest_achievable <= self.spent_this_turn:
            self.wasteless_turns += 1
            wasteless = True
        self.grade_lands_per_turn(wasteless)

    def grade_lands_per_turn(self, wasteless):
        for land in self.played_lands:
            land.turn_appearances += 1
            if wasteless:
                land.wasteless_turns += 1







    def purge_lumps(self, lumps:list[Lump]) -> list[Lump]:
        l = [lump for lump in lumps if lump.cmc <= self.turn]
        l.sort(key=lambda x: x.cmc, reverse=True)
        return l

    def provides_most_colours(self, input:list, library=False):

        #print(f"372: battlefield contains {self.battlefield.lands_list()}, hand contains {self.hand.lands_list()}")
        if len(input) == 0:
            return input
        needed = []
        for lump in self.spell_lumps:
            #print(f"\t To seek for {lump}: {lump.mana_to_seek()}")
            for c in lump.mana_to_seek():
                if c not in needed:
                    needed.append(c)
        #print(f"372:{needed}: in hand, {self.hand.card_list}, on battlefield {self.battlefield.lands_list()} ")
        graded_lands = {}
        for land in input:
            produced = land.live_prod(self)
            #find the land that has the most colours in common with this
            absent = list(set(needed) - set(produced))
            graded_lands[land] = len(absent)
        the_minimum = graded_lands[min(graded_lands, key=lambda option: graded_lands[option])]
        the_minima = []
        for land in graded_lands:
            if graded_lands[land] == the_minimum:
                the_minima.append(land)
        return the_minima

    #generic functions

    def sum_pips(self, inpone, inptwo):
        output = {}
        for x in inpone:
            output[x] = inpone[x] + inptwo[x]
        return output

    def subtract_pips(self, sub_from, sub_this):
        output = {}
        for x in sub_from:
            result = sub_from[x] - sub_this[x]
            output[x] = max(0, result)
        return output







