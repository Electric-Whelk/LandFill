from Extensions import db
from typing import List

class Cycle(db.Model):
    __tablename__ = 'cycles'
    _id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String, nullable=False, unique=True)
    _regex = db.Column(db.String, nullable=False)
    _official = db.Column(db.Boolean, nullable=False)
    _category = db.Column(db.String, nullable=False)
    _synergy = db.Column(db.String, nullable=False)
    _typed = db.Column(db.Boolean, nullable=False)
    _fetch = db.Column(db.Boolean, nullable=False)
    _ramp = db.Column(db.Boolean, nullable=False)

    _cards = db.relationship('Card', back_populates='_cycle')

    #getters and setters
    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value

    @property
    def regex(self):
        return self._regex
    @regex.setter
    def regex(self, value):
        self._regex = value

    @property
    def official(self) -> bool:
        return self._official

    @property
    def cards(self) -> List["Card"]:
        return self._cards

    @property
    def synergy(self) -> str:
        return self._synergy

    @property
    def typed(self) -> bool:
        return self._typed

    @property
    def category(self) -> str:
        return self._category

    @property
    def fetch(self) -> bool:
        return self._fetch
    @fetch.setter
    def fetch(self, value):
        self._fetch = value

    @property
    def ramp(self) -> bool:
        return self._ramp


    #app interaction functions
    def to_JSON(self):
        cards_json = [x.to_JSON() for x in self.cards]
        return {
            "id": self.id,
            "name": self.name,
            "regex": self.regex,
            "official": self.official,
            "category": self.category,
            "synergy": self.synergy,
            "typed": self.typed,
            "cards": cards_json
        }
