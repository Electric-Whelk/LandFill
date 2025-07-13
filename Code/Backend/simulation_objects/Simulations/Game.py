import random

from itertools import combinations
from tabnanny import verbose

from simulation_objects.CardCollections.Battlefield import Battlefield
from simulation_objects.CardCollections.CardCollection import CardCollection
from simulation_objects.CardCollections.Deck import Deck
from simulation_objects.CardCollections.Graveyard import Graveyard
from simulation_objects.CardCollections.Hand import Hand
from simulation_objects.GameCards.Land import Land
from simulation_objects.GameCards.SearchLands.FetchLand import FetchLand
from simulation_objects.GameCards.Spell import Spell
from simulation_objects.Misc.Lump import Lump
from simulation_objects.Simulations.Simulation import Simulation



class Game(Simulation):
    def __init__(self, deck, verbose=False):
        Simulation.__init__(self, deck)
        self._hand = Hand()
        self._battlefield = Battlefield()
        self._graveyard = Graveyard()
        self._turn = 0


        #global reset during the turn
        self._lumps = []
        self._spell_lumps = []
        self._secondmain = False

        #dev attributes
        self.verbose = verbose
        self.decisions = 0
        self.total_spent_mana = 0
        self.options_per_turn = 0
        self.total_turns = 7


    #getters
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

    def oor(self, input):
        try:
            return input[0]
        except IndexError:
            return "NONE"

    def sample_hand(self, input:list):
        self.deck.shuffle()
        for term in input:
            for card in self.deck.card_list:
                if card.name == term:
                    self.deck.give(self.hand, card)
                    break



    #run!
    def conclude_game(self):
        zones = [self.hand, self.battlefield, self.graveyard]
        for zone in zones:
            zone.give_all(self.deck)
        self.options_per_turn /= self.total_turns
        self.vprint("Game complete")
        #print(f"Spent {self.total_spent_mana} mana")

    def run(self):
        #self.setup_game()
        samplehand = ["Golgari Rot Farm", "Island", "Mazirek, Kraul Death Priest", "Xavier Sal, Infested Captain"]
        self.sample_hand(samplehand)
        for _ in range(self.total_turns): #SCAFFOLD - number of turns
            self.run_turn()

        self.conclude_game()
        self.turn = 0
        pass

    def play_land(self, land):
        if land is not None:
            self.vprint(f"Playing {land}...")
            self.hand.give(self.battlefield, land)
        else:
            self.vprint("No land to play")


    def play_land_at_random(self):
        lands = [l for l in self.hand.card_list if isinstance(l, Land)]
        if len(lands) > 0:
            self.hand.give(self.battlefield, lands[0])

    def play_lump(self, lump):
        try:
            lump.tap_mana(self)
            for spell in lump.to_cast:
                self.total_spent_mana += spell.cmc[0]
                self.vprint(f"Playing {spell}...")
                self.hand.give(self.battlefield, spell)
        except AttributeError as e:
            self.vprint("No playable lumps")



    def run_turn(self):
        self.turn += 1
        self.battlefield.untap()
        self.draw()
        self.vprint(f"Hand: {self.hand.card_list}")
        self.vprint(f"Battlefield: {self.battlefield.card_list} ")
        self.determine_play()
        #self.play_land_at_random()
        self.move_through_phases()
        self.vprint("")

    def move_through_phases(self):
        self.secondmain = True
        self.tap_unused_lands()
        self.reset_values()

    def mulligan(self):
        if len(self.lands_in_hand) < 3:
            self.hand.give_all(self.deck)
            self.vprint("Mulliganing...")
            return True
        return False




    def setup_game(self):
        deck = self.deck
        deck.shuffle()
        mull = True
        while mull:
            self.draw(7)
            mull = self.mulligan()

    def tap_unused_lands(self):
        for land in self.battlefield.lands_list():
            if not land.tapped:
                land.conclude_turn(self)


    #game actions
    def draw(self, repeats=1):
        for _ in range(repeats):
            self.deck.give_top(self.hand)


    #strategizing algorithms
    def prioritize_tapland(self, input:list[Land], library=False):
        #add a layer so that it prioritizes fetchlands that can get a perm over a current, and fetchlands that can get a current over a leftover
        if library:
            source = self.deck
        else:
            source = self.hand
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
            source.give(self.battlefield, perm[0])
        elif len(current) > 0:
            source.give(self.battlefield, current[0])
        elif len(leftover) > 0:
            source.give(self.battlefield, leftover[0])





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
        fetches_in_hand = [x for x in self.hand.card_list if isinstance(x, FetchLand)]
        if len(fetches_in_hand) > 0:
            max = m = len(self.hand.lands_list()) + len(self.battlefield.lands_list())
            minrange = m + 1


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
                output.extend(self.create_lumps(c))

        #purged_output = self.purge_lumps(output)
        #print(f"{m}: purged {len(output)-len(purged_output)} from {len(output)} lumps ({input})")
        #return purged_output
        return output


    def determine_max_mana(self) -> int:
        return self.turn



    def determine_play(self):
        lands = [x for x in self.hand.card_list if isinstance(x, Land)]
        self.vprint(f"begnning turn {self.turn} with {lands} in hand and {self.battlefield.lands_list()} on battlefield")
        spells = self.hand.spells_list()
        lumps = self.determine_lumps_from_hand(spells)
        self.lumps = lumps
        self.spell_lumps = self.determine_spell_lumps(spells)
        self.vprint(f"identified {len(self.lumps)} lumps")
        #self.vprint(f"Playable cards: {fodder} divisible into {len(lumps)} lumps")

        moots = self.battlefield.permutations
        for lump in lumps:
            lump.parse_moots(moots)

        for lump in self.spell_lumps:
            lump.parse_moots(moots)

        castable = []
        not_castable = []
        for lump in lumps:
            if lump.castable:
                castable.append(lump)
            else:
                not_castable.append(lump)

        """
        moots = self.battlefield.permutations
        for lump in lumps:
            lump.parse_moots(moots)"""

        playoptions = {}

        self.vprint(f"The following {len(castable)} lumps are playable: {castable}")


        for land in lands:
            enabled = [l for l in lumps if l.check_playmaker(self, land)]
            playoptions[land] = len(enabled)
            self.vprint(f"Playing {land} will allow {playoptions[land]} lumps to be played ({enabled})")

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


        #self.play_land(champ)
        self.battlefield.reset_permutations(self)
        new_moots = self.battlefield.permutations
        new_playable = []
        for lump in lumps:
            lump.parse_moots(new_moots)
            if lump.castable:
                new_playable.append(lump)
        self.options_per_turn += len(new_playable)

        lumpchamp = None
        for option in new_playable:
            if lumpchamp == None or option.cmc > lumpchamp.cmc:
                lumpchamp = option
        self.play_lump(lumpchamp)





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







