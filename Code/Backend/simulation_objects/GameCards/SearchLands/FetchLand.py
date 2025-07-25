from .SearchLand import SearchLand
from .. import BasicLand
from ..Land import Land
from collections import Counter

class FetchLand(SearchLand):
    def __init__(self, card, mandatory):
        SearchLand.__init__(self, card, False, mandatory)

    def determine_general_target(self, input:list, game, specific=True):
        lumps = game.spell_lumps
       # if len(lumps) == 0:
            #print(f"(determine general target) calling a fetchland on zero lumps with hand {game.hand.card_list} ")
        needed = []
        for lump in lumps:
            for c in lump.mana_to_seek():
                if c not in needed and game.hand_cant_produce(c, exclude=self):
                    needed.append(c)
        graded_lands = {}
        for land in input:
            produced = land.live_prod(game)
            #find the land that has the most colours in common with this
            absent = list(set(needed) - set(produced))
            graded_lands[land] = len(absent)
        the_minimum = graded_lands[min(graded_lands, key=lambda option: graded_lands[option])]
        the_minima = []
        for land in graded_lands:
            if graded_lands[land] == the_minimum:
                the_minima.append(land)
        game.battlefield.give(game.graveyard, self)
        if len(the_minima) == 0:
            print(f"{self} can identify no lands to crack for")
        if specific:
            game.prioritize_tapland(the_minima, library=True)
        else:
            game.play_land(the_minima[0], library=True)
        #return the_minima
        #print(f"Playing {the_minima}")



    def determine_search_target(self, input:list, game, color):
        lumps = game.spell_lumps
        needed = []
        for lump in lumps:
            for c in lump.mana_to_seek():
                if c != color and game.hand_cant_produce(c, exclude=self):
                    needed.append(c)
        modal = self.parse_modal_output(Counter(needed).most_common())
        for land in input:
            if modal in land.live_prod(game):
                return land
        return input[0]


    def live_prod(self, game) -> list[str]:
        fetchable = self.search_deck(game)
        output = []
        #print(f"{self.name} can produce {fetchable}")
        for card in fetchable:
            if card.enters_untapped(game):
                for color in card.live_prod(game):
                    if color not in output:
                        output.append(color)
        return output

    def filter_monocolours(self, input:list, game):
        max_colors = max(input, key=lambda c: len(c.live_prod(game)))
        if len(max_colors.live_prod(game)) > 1:
            return [x for x in input if len(x.live_prod(game)) > 1]
        else:
            return input



    def search_deck(self, game) -> list[str]:
        output = []
        for card in game.deck.card_list:
            if isinstance(card, Land):
                for landtype in card.landtypes:
                    if landtype in self.searchable:
                        output.append(card)
                        break
        return output

    def fetch(self, game, color=None):
        fetchable = self.search_deck(game)
        if color is None:
            acceptable = fetchable
        elif color == "Any":
            acceptable = [c for c in fetchable if c.enters_untapped(game)]
        else:
            acceptable = [c for c in fetchable if
                          color in c.live_prod(game) and c.enters_untapped(game)]
        if len(acceptable) == 0:
            raise Exception(f"{self.name}'s ability to tap for {color} has been exaggerated; only {fetchable} is fetchable (hand: {game.hand.lands_list()} board: {game.battlefield.lands_list()})")
        no_basics = self.filter_monocolours(acceptable, game)
        if color is None:
            self.determine_general_target(no_basics, game)
            #print(f"General")
        elif color == "Any":
            self.determine_general_target(no_basics, game, specific=False)
        else:
            target = self.determine_search_target(no_basics, game, color)
            #if isinstance(target, BasicLand):
                #print(f"Searching for {target} with hand: {game.hand.card_list} and battlefield: {game.battlefield.lands_list()}")
            #print(f"Fetching {target} as a search target looking for {color} mana")
            #game.deck.give(game.battlefield, target)
            game.battlefield.give(game.graveyard, self)
            game.play_land(target, library=True)
            #print(f"Playing {target}")
            #print(f"Battlefield: {game.battlefield.card_list}")
            #print(f"Hand: {game.hand.card_list}\n")

    def tap_specific(self, game, c_word):
        self.fetch(game, color=c_word)

    def conclude_turn(self, game):
        self.fetch(game)





