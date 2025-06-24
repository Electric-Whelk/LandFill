from Extensions import db
from database_management.DBManager import DBManager
from database_management.models.Card import Card
from database_management.models.Face import Face
from database_management.models.Format import Format


class Deck:
    def __init__(self, input_cards, format, quantity):
        self._format = self.parse_format_from_json(format)
        self._input_cards = self.parse_cards_from_json(input_cards)
        self._lands_requested = self.determine_lands_requested_from_json(quantity)

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

    #setup functions
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

