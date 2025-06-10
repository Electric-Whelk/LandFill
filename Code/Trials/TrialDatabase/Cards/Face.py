from unittest.mock import PropertyMock

from Configure_DB import Base
from functools import cached_property
from sqlalchemy import ForeignKey
from sqlalchemy import Column
from sqlalchemy.orm import Mapped, declared_attr
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing import Dict
from typing import List

class Face(Base):
    __tablename__ = "faces"

    _id: Mapped[int] = mapped_column(primary_key=True)
    _card_id: Mapped[int] = mapped_column(ForeignKey('cards._id'), nullable=False)
    _name: Mapped[str] = mapped_column(nullable=False)
    _typeline: Mapped[str] = mapped_column(nullable=False)
    _text: Mapped[str] = mapped_column(nullable=True)
    _w: Mapped[int] = mapped_column(nullable=False)
    _u: Mapped[int] = mapped_column(nullable=False)
    _b: Mapped[int] = mapped_column(nullable=False)
    _r: Mapped[int] = mapped_column(nullable=False)
    _g: Mapped[int] = mapped_column(nullable=False)
    _c: Mapped[int] = mapped_column(nullable=False)
    _gen: Mapped[int] = mapped_column(nullable=False)
    _x: Mapped[int] = mapped_column(nullable=False)
    _s: Mapped[int] = mapped_column(nullable=False)
    _playable: Mapped[bool] = mapped_column(nullable=False)
    _land: Mapped[bool] = mapped_column(nullable=False)

    _card: Mapped["Card"] = relationship(back_populates="_faces")


    #override methods
    def __repr__(self):
        return self.name

    #getters and setters corresponding directly to data stored in the table
    @property
    def id(self) -> int:
        return self._id

    @property
    def card_id(self) -> int:
        return self._card_id

    @property
    def type(self) -> str:
        return self._type

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
    def white(self) -> int:
        return self._w
    @white.setter
    def white(self, value:int):
        self._w = value

    @property
    def black(self) -> int:
        return self._b
    @black.setter
    def black(self, value:int):
        self._b = value

    @property
    def red(self) -> int:
        return self._r
    @red.setter
    def red(self, value:int):
        self._r = value

    @property
    def green(self) -> int:
        return self._g
    @green.setter
    def green(self, value:int):
        self._g = value

    @property
    def blue(self) -> int:
        return self._u
    @blue.setter
    def blue(self, value:int):
        self._u = value

    @property
    def colorless(self) -> int:
        return self._c
    @colorless.setter
    def colorless(self, value:int):
        self._c = value

    @property
    def x_in_cost(self) -> int:
        return self._x
    @x_in_cost.setter
    def x_in_cost(self, value:int):
        self._x = value

    @property
    def snow(self) -> int:
        return self._s
    @snow.setter
    def snow(self, value:int):
        self._s = value

    @property
    def generic(self):
        return self._gen
    @generic.setter
    def generic(self, value:int):
        self._gen = value

    @property
    def playable(self) -> bool:
        return self._playable
    @playable.setter
    def playable(self, value:bool):
        self._playable = value

    @property
    def land(self) -> bool:
        return self._land
    @land.setter
    def land(self, value:bool):
        self._land = value

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

    #methods used in construction
    def parse_mana_cost(self, cost):
        self.generic = 0
        cost = list(cost)
        dict = {'W': 0, 'U': 0, 'B': 0, 'R': 0, 'G': 0, 'C': 0, 'X': 0, 'S': 0, 'Y': 0, 'Z':0}
        i = 0
        j = 1
        while i < len(cost):
            if cost[i] == "{":
                pip = cost[j]
                if str.isdigit(pip):
                    self.generic = int(pip)
                else:
                    dict[pip] += 1
            i += 1
            j += 1

        self.white = dict['W']
        self.blue = dict['U']
        self.black = dict['B']
        self.red = dict['R']
        self.green = dict['G']
        self.colorless = dict['C']
        self.x_in_cost = dict['X']
        self.snow = dict['S']


    def parse_face_object(self, obj):
        self._name = obj['name']
        self._text = obj['oracle_text']
        self._typeline = obj['type_line']
        self._land = 'Land' in self.cardtypes

        self.parse_mana_cost(obj['mana_cost'])

    #general functions (alphabetized)
    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "text": self.text
        }