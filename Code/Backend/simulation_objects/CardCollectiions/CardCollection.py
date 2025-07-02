from database_management.models.Card import Card
from database_management.models.Cycle import Cycle
from database_management.models.Face import Face
from Extensions import db
from random import shuffle
from simulation_objects.GameCards.BasicLand import BasicLand
from simulation_objects.GameCards.GameCard import GameCard
from simulation_objects.GameCards.Land import Land
from simulation_objects.GameCards.Spell import Spell


class CardCollection:
    def __init__(self):
        self._cards = []

    #getters and setters
    @property
    def card_list(self) -> list[GameCard]:
        return self._cards
    @card_list.setter
    def card_list(self, cards: list[GameCard]):
        self._cards = cards

    #card shifting
    def give(self, recipient:"CardCollection", item:GameCard):
        recipient.receive(item)
        self.card_list.remove(item)

    def give_top(self, recipient:"CardCollection"):
        self.give(recipient, self.card_list[0])

    def receive(self, item:GameCard):
        self.card_list.append(item)

    def shuffle(self):
        shuffle(self.card_list)

    #cards used to add new GameCard objects
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

    def set_card_list_from_ORM(self, cards:list[Card], mandatory=False):
        self.card_list = [self.parse_GameCard(x, mandatory) for x in cards]


    def parse_GameCard(self, card:Card, mandatory=False):
        if not card.overall_land:
            return Spell(card, mandatory)
        else:
            cycle = card.cycle
            text = card.text
            name = cycle.name
            match name:
                case "Basic Lands":
                    return BasicLand(card, mandatory)
                case _:
                    return Land(card, mandatory)

