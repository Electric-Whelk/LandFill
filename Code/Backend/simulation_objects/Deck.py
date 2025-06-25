from Extensions import db
from ColorPie import ColorPie
from database_management.DBManager import DBManager
from database_management.models.Card import Card
from database_management.models.Face import Face
from database_management.models.Format import Format


class Deck:
    def __init__(self, input_cards, format, quantity):
        self._format = self.parse_format_from_json(format)
        self._input_cards = self.parse_cards_from_json(input_cards)
        self._lands_requested = self.determine_lands_requested_from_json(quantity)
        self._color_id = self.determine_color_id()
        self._pips = self.determine_pips()
        self._colors_needed = self.determine_colors_needed()
        self._possible_lands = self.determine_possible_lands()

    #getters and setters
    @property
    def format(self) -> Format:
        return self._format

    @property
    def input_cards(self) -> list[Card]:
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
    def possible_lands(self) -> list:
        return self._possible_lands

    #setup functions
    def determine_color_id(self):
        output = []
        for card in self._input_cards:
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


    def determine_pips(self) -> dict:
        output = {'W': 0, 'U': 0, 'B': 0, 'R': 0, 'G': 0, 'C': 0, 'S': 0}
        for card in self._input_cards:
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
        print(f"queried for {len(all)} lands")
        pie = ColorPie()
        pie.parse_colors(self.colors_needed)
        lands = [x for x in all
                 if pie.produces_needed(x.produced_score.value) and
                 x.produced_score.count > 1]
        print(f"List comprehension returned {len(lands)} lands")
        return lands





    def determine_lands_requested_from_json(self, quantity):
        return int(quantity)

    def get_card_by_name(self, name):
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

