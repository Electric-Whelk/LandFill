from database_management.models.Card import Card

class GameCard(object):
    def __init__(self, card, start_zone):
        self._name = card.name
        self._usd = card.usd
        self._eur = card.eur

        self._zone = start_zone


    #getters and setters
    @property
    def name(self):
        return self._name

    @property
    def zone(self) -> str:
        return self._zone
    @zone.setter
    def zone(self, value:str):
        self._zone = value

    @property
    def usd(self):
        return self._usd

    @property
    def eur(self):
        return self._eur

