from database_management.models.Card import Card
from database_management.models.Cycle import Cycle
from currency_converter import CurrencyConverter

class GameCard(object):
    def __init__(self, card:Card, mandatory=False, permitted = True):
        self._name = card.name
        self._usd = float(card.usd) / 100
        self._eur = float(card.eur) / 100
        self._gbp = 0
        self._color_id = list(card._color_identity)
        self._text = self.parse_text(card)
        self._image = None
        self._off_color_fetch = False


        self._mandatory = mandatory
        self._permitted = permitted
        self._tapped = False


    def __repr__(self):
        return self._name


    #getters and setters
    @property
    def off_color_fetch(self):
        return self._off_color_fetch
    @off_color_fetch.setter
    def off_color_fetch(self, value):
        self._off_color_fetch = value

    @property
    def image(self):
        return self._image
    @image.setter
    def image(self, value):
        self._image = value

    @property
    def text(self):
        return self._text

    @property
    def color_id(self) -> list:
        return self._color_id

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
    def gbp(self):
        return self._gbp
    @gbp.setter
    def gbp(self, value):
        self._gbp = value

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


    def to_dict(self):
         return {
            "name": self.name,
            "USD": self.usd,
            "EUR": self.eur,
            "GBP": round(self.gbp, 2),
            "mandatory": self.mandatory,
            "permitted": self.permitted,
            "image": self.image,
            "offColorFetch": self.off_color_fetch
        }

    def parse_text(self, card) -> str:
        if len(card.faces) == 1:
            return card.faces[0].text
        else:
            return f"{card.faces[0].text} // {card.faces[1].text}"



