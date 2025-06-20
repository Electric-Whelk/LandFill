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
    def cards(self) -> List["Card"]:
        return self._cards

    @property
    def synergy(self):
        return self._synergy