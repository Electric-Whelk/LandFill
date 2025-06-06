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
    _text: Mapped[str] = mapped_column(nullable=False)
    _type: Mapped[str] = mapped_column(nullable=False)

    _card: Mapped["Card"] = relationship(back_populates="_faces")

    __mapper_args__ = {
        "polymorphic_on": _type,
        "polymorphic_identity": "base_face",
    }

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
    def type(self):
        return self._type


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





    def parse_face_object(self, obj):
        self._name = obj['name']
        self._text = obj['oracle_text']
        self._typeline = obj['type_line']




    """
    FOR POSTERITY - this was the mixin class approach
    @declared_attr
    def _id(cls) -> Mapped[int]:
        return mapped_column(primary_key=True)

    @declared_attr
    def _card_id(cls) -> Mapped[int]:
        return mapped_column(ForeignKey('cards._id'), nullable=False)

    @declared_attr
    def _name(cls) -> Mapped[str]:
        return mapped_column(nullable=False)

    @declared_attr
    def _typeline(cls) -> Mapped[str]:
        return mapped_column(nullable=False)

    @declared_attr
    def _text(cls) -> Mapped[str]:
        return mapped_column(nullable=False)

    @declared_attr
    def _card(cls) -> Mapped["Card"]:
        return relationship("Card",back_populates="_faces")
    """