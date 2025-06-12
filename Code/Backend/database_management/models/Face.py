from functools import cached_property
from Extensions import db
from typing import List, Dict

class Face(db.Model):
    __tablename__ = 'faces'
    _id = db.Column(db.Integer, primary_key=True)
    _card_id = db.Column(db.Integer, db.ForeignKey('cards._id'))
    _name = db.Column(db.String, nullable=False, unique=True)
    _typeline = db.Column(db.String, nullable=False)
    _text = db.Column(db.String, nullable=True)
    _playable = db.Column(db.Boolean, nullable=False)
    _land = db.Column(db.Boolean, nullable=False)
    _mana_cost = db.Column(db.String, nullable=False)

    _card = db.relationship('Card', back_populates="_faces")

    #setters and getters
    @property
    def id(self) -> int:
        return self._id

    @property
    def card_id(self) -> int:
        return self._card_id

    @property
    def name(self) -> str:
        return self._name
    @name.setter
    def name(self, value:str):
        self._name = value

    @property
    def typeline(self) -> str:
        return self._typeline
    @typeline.setter
    def typeline(self, value:str):
        self._typeline = value

    @property
    def text(self) -> str:
        return self._text
    @text.setter
    def text(self, value:str):
        self._text = value

    @property
    def playable(self) -> bool:
        return self._playable
    @playable.setter
    def playable(self, value: bool):
        self._playable = value

    @property
    def land(self) -> bool:
        return self._land
    @land.setter
    def land(self, value: bool):
        self._land = value

    @property
    def mana_cost(self) -> str:
        return self._mana_cost
    @mana_cost.setter
    def mana_cost(self, value:str):
        self._mana_cost = value

    #cached properties
    @cached_property
    def parsed_types(self) -> Dict[str, List[str]]:
        supertypes = []
        types = []
        subtypes = []
        known_supertypes = ["Basic", "Legendary", "Ongoing", "Snow", "World"]

        space_split = self.typeline.split(" ")
        while space_split[0] in known_supertypes:
            supertypes.append(space_split.pop(0))

        while len(space_split) > 0 and space_split[0] != "—":
            types.append(space_split.pop(0))

        if len(space_split) != 0:
            space_split.pop(0)
            subtypes = space_split

        return {"supertypes": supertypes, "cardtypes": types, "subtypes": subtypes}

    #setter and getter functions that work with cached properties
    @property
    def cardtypes(self) -> List[str]:
        return self.parsed_types["cardtypes"]

    @property
    def subtypes(self) -> List[str]:
        return self.parsed_types["subtypes"]

    @property
    def supertypes(self) -> List[str]:
        return self.parsed_types["supertypes"]

    #scrython object parsing functions
    def parse_face_object(self, obj):
        self._name = obj['name']
        self._text = obj['oracle_text']
        self._typeline = obj['type_line']
        self._land = 'Land' in self.cardtypes

        self.mana_cost = obj['mana_cost']
