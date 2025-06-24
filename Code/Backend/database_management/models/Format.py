import json

from database_management.models.Intermediates import Banned, Restricted, Legal, GameFormats
from Extensions import db


class Format(db.Model):
    __tablename__ = 'formats'
    _id = db.Column(db.Integer, primary_key=True)
    _display_name = db.Column(db.String, nullable=False, unique=True)
    _scryfall_name = db.Column(db.String, nullable=False)
    _copies = db.Column(db.Integer, nullable=False)
    _deck_size = db.Column(db.Integer, nullable=False)
    _hard_max = db.Column(db.Boolean, nullable=False)
    _arena = db.Column(db.Boolean, nullable=False)
    _mtg_online = db.Column(db.Boolean, nullable=False)
    _paper = db.Column(db.Boolean, nullable=False)

    _banned = db.relationship('Card',
                              secondary=Banned.__table__,
                              back_populates='_banned',
                              passive_deletes=True)
    _restricted = db.relationship('Card',
                                  secondary=Restricted.__table__,
                                  back_populates='_restricted',
                                  passive_deletes=True)
    _legal = db.relationship('Card',
                             secondary=Legal.__table__,
                             back_populates='_legal',
                             passive_deletes=True)

    _games = db.relationship('Game',
                             secondary=GameFormats.__table__,
                             back_populates='_formats',
                             passive_deletes=True)

    #setters and getters
    @property
    def id(self):
        return self._id

    @property
    def display_name(self) -> str:
        return self._display_name
    @display_name.setter
    def display_name(self, value:str):
        self._display_name = value

    @property
    def scryfall_name(self) -> str:
        return self._scryfall_name
    @scryfall_name.setter
    def scryfall_name(self, value:str):
        self._scryfall_name = value

    @property
    def copies(self) -> int:
        return self._copies
    @copies.setter
    def copies(self, value:int):
        self._copies = value

    @property
    def deck_size(self) -> int:
        return self._deck_size

    @property
    def hard_max(self) -> bool:
        return self._hard_max

    @property
    def arena(self) -> bool:
        return self._arena

    @property
    def mtg_online(self) -> bool:
        return self._mtg_online

    @property
    def paper(self) -> bool:
        return self._paper

    @property
    def banned(self) -> bool:
        return self._banned

    @property
    def restricted(self) -> bool:
        return self._restricted

    @property
    def legal(self) -> bool:
        return self._legal

    @property
    def games(self) -> int:
        return self._games



    #App Interaction Functions
    def to_JSON(self):
        return {
            'id': self.id,
            'display_name': self.display_name,
            'scryfall_name': self.scryfall_name,
            'copies': self.copies,
            'deck_size': self.deck_size,
            'hard_max': self.hard_max,
            'arena': self.arena,
            'mtg_online': self.mtg_online,
            'paper': self.paper,
        }





