from Extensions import db
from database_management.models.Intermediates import GameCards, GameFormats


class Game(db.Model):
    __tablename__ = 'games'
    _id = db.Column(db.Integer, primary_key=True)
    _display_name = db.Column(db.String, nullable=False, unique=True)
    _scryfall_name = db.Column(db.String, nullable=False)

    _cards = db.relationship('Card',
                             secondary=GameCards.__table__,
                             back_populates='_games',
                             passive_deletes=True)
    _formats = db.relationship('Format',
                               secondary=GameFormats.__table__,
                               back_populates='_games',
                               passive_deletes=True)

    @property
    def scryfall_name(self) -> str:
        return self._scryfall_name
    @scryfall_name.setter
    def scryfall_name(self, value:str):
        self._scryfall_name = value