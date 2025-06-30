from Extensions import db
from ColorPie import ColorPie
from database_management.DBManager import DBManager
from database_management.models.Card import Card
from database_management.models.Face import Face
from database_management.models.Format import Format
from simulation_objects.CardCollection import CardCollection
from simulation_objects.GameCard import GameCard
from simulation_objects.Land import Land
from simulation_objects.Spell import Spell




class Deck(CardCollection):
    def __init__(self):
        self._lands_requested = None

    def setup(self, input_cards, format, quantity):
        self._format = self.parse_format_from_json(format)

        input_as_cards = self.parse_cards_from_json(input_cards)
        self._input_cards = [self.parse_GameCards(x, "deck") for x in input_as_cards]
        self._lands_requested = self.determine_lands_requested_from_json(quantity)
        self._size = self.determine_size()
        self._color_id = self.determine_color_id(input_as_cards)
        self._pips = self.determine_pips(input_as_cards)
        self._colors_needed = self.determine_colors_needed()
        self._possible_lands = self.determine_possible_lands()

    #getters and setters

    @property
    def format(self) -> Format:
        return self._format

    @property
    def input_cards(self) -> list[GameCard]:
        return self._input_cards

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

    #setup functions
    def determine_color_id(self, input_as_cards):
        output = []
        for card in input_as_cards:
            id = list(card.color_identity)
            for color in id:
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
                        lands.append(self.parse_GameCards(card, "heap"))
                        break
        return lands

    def determine_size(self) -> int:
        inp = len(self._input_cards)
        req = self.lands_requested
        return inp + req


    def get_card_by_name(self, name) -> Card:
        face = db.session.query(Face).filter(Face._name == name).first()
        card = db.session.query(Card).filter(Card._id == face.card_id).first()
        return card

    def parse_cards_from_json(self, cards):
        as_list = cards.split("\n")
        output = []
        for name in as_list:
            card = self.get_card_by_name(name)
            output.append(card)
        return output

    def parse_format_from_json(self, format):
        return db.session.query(Format).filter(Format._id == format["id"]).first()



    #misc functions
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

