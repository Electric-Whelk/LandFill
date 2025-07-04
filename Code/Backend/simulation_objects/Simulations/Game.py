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

        #def attributes
        self.verbose = True

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

    #dev methods
    def vprint(self, input):
        if self.verbose:
            print(input)

    #run!
    def run(self):
        self.setup_game()
        for _ in range(4): #SCAFFOLD - number of turns
            self.run_turn()

        self.vprint("Game complete")
        self.turn = 0
        pass

    def play_land_at_random(self):
        self.deck.give(self.battlefield, [l for l in self.deck.card_list if isinstance(l, Land)][0])

    def run_turn(self):
        self.turn += 1
        self.vprint(f"Beginning turn {self.turn} with max mana {self.max_mana}")
        self.battlefield.untap()
        self.draw()
        self.vprint(f"Hand: {self.hand.card_list}")
        self.play_land_at_random()
        self.vprint(f"Battlefield: {self.battlefield.card_list} ")
        self.determine_play()
        self.vprint("")

    def setup_game(self):
        deck = self.deck
        deck.shuffle()
        self.draw(7)


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

    def determine_lumps_from_hand(self, input:list[Spell]) -> list[Lump]:
        output = []
        l = len(input)
        for r in range(1, l+1):
            for c in combinations(input, r):
                output.extend(self.create_lumps(c))
        purged_output = self.purge_lumps(output)
        return purged_output


        """        
        output = []
        output.extend(self.create_lumps(input))
        if len(input) == 1:
            return output

        versions = []
        for spell in input:
            versions.append([x for x in input if x != spell])
        for version in versions:
            determined = self.determine_lumps_from_hand(version)
            for lump in determined:
                if len(lump.to_cast) != 1
            output.extend(self.determine_lumps_from_hand(version))
        return output

        """

    def determine_max_mana(self) -> int:
        return self.turn



    def determine_play(self):
        max = self.determine_max_mana()
        fodder = [x for x in self.hand.spells_list() if x.cmc[0] <= max]
        print(f"Playable cards: {fodder}")
        lumps = self.determine_lumps_from_hand(fodder)
        info = self.battlefield.mana_combinations(self)
        for mlump in info:
            print(f"{[m["color"] for m in mlump]}")
        #self.vprint(f"Available mana: {[[x:["color"] for x in ] ]}")

        pass

    def purge_lumps(self, lumps:list[Lump]) -> list[Lump]:
        l = [lump for lump in lumps if lump.cmc <= self.max_mana]
        l.sort(key=lambda x: x.cmc, reverse=True)
        return l







        pass





    #card simulation

    def can_I_play_this(self, suggestions:list[Spell], extra_land:Land = None):
        untapped = [x for x in self.battlefield.card_list if x.untapped]
        if extra_land is not None:
            if self.does_it_enter_tapped(extra_land):
                untapped.append(extra_land)





    def does_it_enter_tapped(self, input:Land):
        pass





