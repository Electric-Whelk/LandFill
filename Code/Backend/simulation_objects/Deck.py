from Extensions import db
from database_management.DBManager import DBManager
from database_management.models.Card import Card
from database_management.models.Face import Face
from database_management.models.Format import Format


class Deck:
    def __init__(self, input_cards, format, quantity):
        self._format = self.parse_format_from_json(format)
        self._input_cards = self.parse_cards_from_json(input_cards)
        self._deck_size = self.determine_deck_size_from_quantity(quantity)

    #getters and setters
    @property
    def format(self) -> Format:
        return self._format

    @property
    def input_cards(self) -> list[Card]:
        return self._input_cards

    @property
    def deck_size(self) -> int:
        return self._deck_size

    #setup functions
    def determine_deck_size_from_quantity(self, quantity):
        pass

    def parse_cards_from_json(self, cards):
        as_list = cards.split("\n")
        for name in as_list:
            db.session.query(Face).filter(Face._name == name).first()
        pass

    def parse_format_from_json(self, format):
        return db.session.query(Format).filter(Format._id == format["id"]).first()

