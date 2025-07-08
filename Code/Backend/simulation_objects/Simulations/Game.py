import random

from itertools import combinations
from simulation_objects.CardCollections.Battlefield import Battlefield
from simulation_objects.CardCollections.CardCollection import CardCollection
from simulation_objects.CardCollections.Deck import Deck
from simulation_objects.CardCollections.Graveyard import Graveyard
from simulation_objects.CardCollections.Hand import Hand
from simulation_objects.GameCards.Land import Land
from simulation_objects.GameCards.Spell import Spell
from simulation_objects.Misc.Lump import Lump
from simulation_objects.Simulations.Simulation import Simulation


class Game(Simulation):
    def __init__(self, deck):
        Simulation.__init__(self, deck)
        self._hand = Hand()
        self._battlefield = Battlefield()
        self._graveyard = Graveyard()
        self._turn = 0


        #metrics

        #dev attributes
        self.verbose = False
        self.decisions = 0
        self.total_spent_mana = 0
        self.options_per_turn = 0
        self.total_turns = 7

    #getters
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

    def run(self):
        self.setup_game()
        #samplehand = ["Plains", "Plains", "Vindicate", "Swamp", "Wayfarer's Bauble", "Utter End", "Ayli, Eternal Pilgrim"]
        #self.sample_hand(samplehand)
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
            for spell in lump.to_cast:
                self.total_spent_mana += spell.cmc[0]
                self.vprint(f"Playing {spell}...")
                self.hand.give(self.battlefield, spell)
        except AttributeError:
            self.vprint("No playable lumps")
            pass


    def run_turn(self):
        self.turn += 1
        self.battlefield.untap()
        self.draw()
        self.vprint(f"Hand: {self.hand.card_list}")
        self.vprint(f"Battlefield: {self.battlefield.card_list} ")
        hey = self.determine_play()
        #self.play_land_at_random()
        self.vprint("")

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


    #game actions
    def draw(self, repeats=1):
        for _ in range(repeats):
            self.deck.give_top(self.hand)


    #strategizing algorithms
    def create_lumps(self, input:list[Spell]) -> list[Lump]:
        #draft version that picks a MDFC output randomly, but there is room to improve here by getting all MDFC permutations
        fodder = {}
        for spell in input:
            if len(spell.mana) == 1:
                fodder[spell] = 0
            else:
                fodder[spell] = random.randint(0, 1)
        return [Lump(fodder)]

    def determine_lumps_from_hand(self, input:list[Spell], max:int) -> list[Lump]:
        output = []
        l = len(input)
        #print(f"Max: {self.battlefield.max_mana()}")
        #l bpm = 66
        #self.battlefield.max_mana bpm = 109
        #never more than 3 = can no longer keep count
        m = self.turn

        for r in range(1, min(m, 3) + 1):
            #print(f"R: {r}")
            combos = combinations(input, r)
            #as_list = list(combos)
            #print(f"Combos returned {len(as_list)} combos for range {r}, one of which is {as_list[0]}")
            for c in combos:
                output.extend(self.create_lumps(c))
        purged_output = self.purge_lumps(output)
        #print(f"{m}: purged {len(output)-len(purged_output)} from {len(output)} lumps ({input})")
        return purged_output


    def determine_max_mana(self) -> int:
        return self.turn



    def determine_play(self):
        max = self.battlefield.max_mana() + 1
        lands = [x for x in self.hand.card_list if isinstance(x, Land)]
        self.vprint(f"begnning turn {self.turn} with the following lands: {lands}")
        fodder = [x for x in self.hand.spells_list() if x.cmc[0] <= max]
        lumps = self.determine_lumps_from_hand(fodder, max)
        self.vprint(f"Playable cards: {fodder} divisible into {len(lumps)} lumps")
        for lump in lumps:
            self.vprint(f"\t{lump}")
        #for lump in lumps:
            #self.battlefield.mana_combinations(self, lump)


        #if len(lumps) < 1:
            #return 0

        moots = self.battlefield.mana_permutations(self)
        for lump in lumps:
            lump.parse_moots(moots)

        castable = []
        not_castable = []
        for lump in lumps:
            if lump.castable:
                castable.append(lump)
            else:
                not_castable.append(lump)




        almost_playable = []
        playable = []
        for lump in lumps:
            if lump.cmc == self.turn - 1:
                playable.append(lump)
            if lump.cmc == self.turn:
                almost_playable.append(lump)
        #self.vprint(f"{len(playable)} playable lumps including {self.oor(playable)}")
        #self.vprint(f"{len(almost_playable)} almost playable lumps including {self.oor(almost_playable)}")
        
        
        moots = self.battlefield.mana_permutations(self)
        for lump in lumps:
            lump.parse_moots(moots)

        playoptions = {}

        self.vprint(f"The following {len(castable)} lumps are playable: {castable}")

        for land in lands:
            enabled = [l for l in lumps if l.check_playmaker(self, land)]
            playoptions[land] = len(enabled)
            self.vprint(f"Playing {land} will allow {playoptions[land]} lumps to be played ({enabled})")

        champ = None
        for option in playoptions:
            if champ == None:
                champ = option
            elif playoptions[option] > playoptions[champ]:
                champ = option
                self.decisions += 1

        self.play_land(champ)
        new_moots = self.battlefield.mana_permutations(self)
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






        """
        print("The following lumps are playable:")
        for lump in lumps:
            if lump.castable:
                print(f"\t{lump}")
        print("The following lumps are playable if provided with the following mana")
        for lump in [l for l in lumps if not l.castable]:
            print(f"\t{lump}")
            for moot in lump.moots:
                print(f"\t{moot._generic} generic mana plus {moot._pips}")"""
                #rint(f"{lump} - can be cast with one more mana of any color")
           # else:
                #print(f"{lump} - can be cast with the addition of {lump.playmakers}")
            #print(f"{lump} - playable: {lump.castable}, needs {lump.playmakers}")

        #for lump in almost_playable:
            #self.battlefield.encode_lump(self, lump)
            #print(f"Add {lump.playmakers} to play {lump}")


        #testlump = lumps[random.randint(0, len(lumps) - 1)]
        #for lump in lumps:
            #print(lump)
        #self.vprint(f"Test lump (one of {len(lumps)}: {testlump}")
        #self.battlefield.encode_lump(self, testlump)
        #moots = self.battlefield.mana_permutations(self)
        return 1

        #for lump in lumps:
            #self.can_I_play_this(lump)
        #info = self.battlefield.mana_combinations(self, n=3)
        #for mlump in info:
            #print(f"we get: {mlump}")
        #self.vprint(f"Available mana: {[[x:["color"] for x in ] ]}")

        pass

    def purge_lumps(self, lumps:list[Lump]) -> list[Lump]:
        l = [lump for lump in lumps if lump.cmc <= self.turn]
        l.sort(key=lambda x: x.cmc, reverse=True)
        return l




    #card simulation

    def can_I_play_this(self, lump):
        info = self.battlefield.encode_lump(self, )







    def does_it_enter_tapped(self, input:Land):
        pass





