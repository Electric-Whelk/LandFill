from math import floor
from itertools import combinations

import numpy as np

from Extensions import db
from database_management.models.Card import Card
from database_management.models.Face import Face
from database_management.models.Format import Format
from simulation_objects.CardCollections.CardCollection import CardCollection
from simulation_objects.GameCards.GameCard import GameCard
from simulation_objects.GameCards.Land import Land


class Deck(CardCollection):
    def __init__(self):
        CardCollection.__init__(self)
        self._lands_requested = None

    def setup(self, input_cards, format, quantity, commander_name, partner=None):
        self._format = self.parse_format_from_json(format)

        input_as_cards = self.parse_cards_from_json(input_cards)
        self.set_card_list_from_ORM(input_as_cards, mandatory=True)
        self.set_commanders(commander_name, partner=partner)

        self._lands_requested = self.determine_lands_requested_from_json(quantity)
        self._size = self.determine_size()
        self._color_id = self.determine_color_id()
        self._pie_slices = self.slice_the_pie(self._color_id)
        self._pips = self.determine_pips(input_as_cards)
        self._colorless_pips = self._pips["C"] > 0
        self._colors_needed = self.determine_colors_needed()
        self._possible_lands = self.determine_possible_lands()


    #getters and setters
    @property
    def pie_slices(self):
        return self._pie_slices

    @property
    def colorless_pips(self):
        return self._colorless_pips

    @property
    def format(self) -> Format:
        return self._format

    @property
    def lands_requested(self) -> int:
        return self._lands_requested

    @property
    def color_id(self) -> str:
        return self._color_id

    @property
    def pips(self) -> dict:
        return self._pips

    @property
    def colors_needed(self) -> list:
        return self._colors_needed

    @property
    def possible_lands(self) -> list[Land]:
        return self._possible_lands

    @property
    def size(self) -> int:
        return self._size

    @property
    def commander(self):
        return self._commander

    @property
    def partner(self):
        return self._partner

    #setup functions
    def slice_the_pie(self, color_id:list):
        output = []
        for r in range(2, len(color_id) + 1):
            #print(f"R: {r}")
            combos = list(combinations(color_id, r))
            for c in combos:
                output.append(list(c))
        return output

    def set_commanders(self, commander_name, partner=None):
        commander = self.create_commander_gamecard(commander_name)
        if partner is not None:
            partner = self.create_commander_gamecard(partner)
        self._commander = commander
        self._partner = partner


    def create_commander_gamecard(self, name):
        as_card = self.get_card_by_name(name)
        as_gamecard = self.parse_GameCard(as_card, mandatory=True, commander=True)
        self.card_list.append(as_gamecard)
        return as_gamecard


    def determine_color_id_CONDEMNED(self, input_as_cards):
        output = []
        for card in input_as_cards:
            id = list(card.color_identity)
            for color in id:
                if color not in output:
                    output.append(color)
        print(f"Id: {output}")
        return output

    def determine_color_id(self):
        output = [x for x in self.commander.color_id]
        if self.partner is not None:
            for color in self.partner.color_id:
                if color not in output:
                    output.append(color)
        return output




    def determine_colors_needed(self) -> list:
        all_colors = ["W", "U", "B", "R", "G", "C"]
        pips = self._pips
        as_list = [c for c in all_colors if pips.get(c) > 0]
        return as_list


    def determine_lands_requested_from_json(self, quantity):
        return int(quantity)

    def determine_pips(self, input_as_cards) -> dict:
        output = {'W': 0, 'U': 0, 'B': 0, 'R': 0, 'G': 0, 'C': 0, 'S': 0}
        for card in input_as_cards:
            for face in card.faces:
                cost = list(face.mana_cost)
                i = 0
                j = 1
                while i < len(cost):
                    if cost[i] == "{":
                        pip = cost[j]
                        try:
                            output[pip] += 1
                        except KeyError:
                            pass
                    i += 1
                    j += 1
        #print(f"output: {output}")

        return output


    def determine_possible_lands(self) -> list:
        all = db.session.query(Card).filter(Card._overall_land == True).all()
        lands = []
        for card in all:
            if len(card.true_produced) != 0:
                match = 0
                for color in card.true_produced:
                    if color in self.colors_needed:
                        match += 1
                    if match >= 2:
                        lands.append(self.parse_GameCard(card))
                        break
        return lands

    def determine_size(self) -> int:
        inp = len([x for x in self.card_list if x.mandatory])
        req = self.lands_requested
        return inp + req

    def parse_format_from_json(self, format):
        return db.session.query(Format).filter(Format._id == format["id"]).first()



    #misc functions
    def full(self) -> bool:
        return len(self.card_list) >= self.size

    def get_all_lands(self) -> list[Card]:
        print("Getting lands...")
        lands = db.session.query(Card).filter(Card._overall_land == True)
        print("all lands retrieved...")
        multicolor = lands.filter(Card._produced == "R")
        for card in list(multicolor):
            print(card._name)
        return list(multicolor)


    def permutate(self, input:list):
        primes = {"W": 2, "U": 3, "B": 5, "R": 7, "G": 11, "C": 13}
        c_val = 1
        pass

    def add_initial_lands(self, type):
        match type:
            case "proportional_basics":
                self.add_proportional_basics()
            case _:
                raise Exception("Invalid input to Deck.add_initial_lands()")



    def add_proportional_basics(self):
        proportionalized = self.proportions(self.pips, self.lands_requested)
        as_string = self.determine_basics_from_dict(proportionalized)
        as_cards = self.parse_cards_from_json(as_string)
        self.card_list.extend([self.parse_GameCard(x, mandatory=False) for x in as_cards])

    def proportions(self, pips, lands_requested):
        # Filter out colors with zero need
        filtered_needs = {color: amount for color, amount in pips.items() if amount > 0}
        total_mana = sum(filtered_needs.values())

        # Get raw land counts (floored), and remainders for rounding
        raw_lands = {color: amount / total_mana * lands_requested for color, amount in filtered_needs.items()}
        floored_lands = {color: floor(val) for color, val in raw_lands.items()}
        remainders = {color: raw_lands[color] - floored_lands[color] for color in raw_lands}

        # Distribute remaining lands based on highest remainder
        lands_allocated = sum(floored_lands.values())
        lands_to_allocate = lands_requested - lands_allocated

        for color, _ in sorted(remainders.items(), key=lambda x: x[1], reverse=True)[:lands_to_allocate]:
            floored_lands[color] += 1

        return floored_lands

    def within_color_identity(self, card:Card) -> bool:
        as_list = list(card._color_identity)
        output = True
        for color in as_list:
            if color not in self.color_id:
                return False
        return True




