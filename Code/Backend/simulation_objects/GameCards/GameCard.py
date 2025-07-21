from database_management.models.Card import Card

class GameCard(object):
    def __init__(self, card:Card, mandatory=False, permitted = True):
        self._name = card.name
        self._usd = card.usd
        self._eur = card.eur

        self._mandatory = mandatory
        self._permitted = permitted
        self._tapped = False


    def __repr__(self):
        return self._name


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
    def permitted(self) -> bool:
        return self._permitted
    @permitted.setter
    def permitted(self, value:bool):
        self._permitted = value

    @property
    def tapped(self) -> bool:
        return self._tapped
    @tapped.setter
    def tapped(self, value:bool):
        self._tapped = value

    def produced_quantity(self) -> int:
        return 0

    def can_produce(self, color:str, game) -> bool:
        return False

    def parse_modal_output(self, input) -> str:
        if input == []:
            return "Not A Color"
        return input[0][0]



