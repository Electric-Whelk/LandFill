from database_management.models.Card import Card

class GameCard(object):
    def __init__(self, card, mandatory=False):
        self._name = card.name
        self._usd = card.usd
        self._eur = card.eur

        self._mandatory = mandatory
        self._tapped = False


    #getters and setters
    @property
    def name(self):
        return self._name

    @property
    def usd(self):
        return self._usd

    @property
    def eur(self):
        return self._eur

    @property
    def mandatory(self) -> bool:
        return self._mandatory
    @mandatory.setter
    def mandatory(self, value:bool):
        self._mandatory = value

    @property
    def tapped(self) -> bool:
        return self._tapped
    @tapped.setter
    def tapped(self, value:bool):
        self._tapped = value

