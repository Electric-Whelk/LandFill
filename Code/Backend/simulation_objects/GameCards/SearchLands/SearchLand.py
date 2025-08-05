from simulation_objects.GameCards.Land import Land

class SearchLand(Land):
    def __init__(self, card, basic_only, mandatory=False, **kwargs):
        Land.__init__(self, card, mandatory, **kwargs)
        self._basic_only = basic_only
        self._searchable = card.check_searched_lands_comprehensive()
        self._generic_price = 1
        self._none_price = 0
        #print(f"{self.name}:{self.searchable}")

    @property
    def basic_only(self):
        return self._basic_only

    @property
    def searchable(self):
        return self._searchable

    def ranking_category(self, monty):
        return ["SearchLand"]

    def tap_for_specific_v2(self, color, game):
        searchable = self.get_searchable_lands(game)
        if color == "None":
            acceptable = searchable
        elif color == "Gen":
            acceptable = [c for c in searchable if c.enters_untapped(game)]
        else:
            acceptable = [c for c in searchable if
                          color in c.live_prod(game) and c.enters_untapped(game)]

        most_colors = game.filter_by_most_produced(acceptable, library=True)
        taplands_prioritized = game.filter_as_taplands(most_colors)
        game.battlefield.give(game.graveyard, self)
        try:
            target = taplands_prioritized[0]
            game.play_land_v2(target, library=True)
        except ValueError:
            print(f"Had no fetch options on battlefield {game.battlefield.cards_list} and hand {game.hand.cards_list}")
        except IndexError:
            print(f"Had no fetch options on battlefield {game.battlefield.cards_list} and hand {game.hand.cards_list}")




    def get_searchable_lands(self, game):
        return [x for x in game.deck.card_list if x.name in self.searchable]

    def can_find(self, subject):
        return subject.name in self.searchable







