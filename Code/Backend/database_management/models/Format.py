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

    _banned = db.relationship('Card', secondary=Banned.__table__, back_populates='_banned')
    _restricted = db.relationship('Card', secondary=Restricted.__table__, back_populates='_restricted')
    _legal = db.relationship('Card', secondary=Legal.__table__, back_populates='_legal')

    _games = db.relationship('Game', secondary=GameFormats.__table__, back_populates='_formats')

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




