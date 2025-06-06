from operator import truediv

from Cards.Face import Face
from Cards.SpellFace import SpellFace
from Cards.LandFace import LandFace
from Configure_DB import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing import List


class Card(Base):
    __tablename__ = 'cards'

    _id: Mapped[int] = mapped_column(primary_key=True)
    _name: Mapped[str] = mapped_column(unique=True, nullable=False)
    _usd: Mapped[float] = mapped_column(nullable=False)
    _eur: Mapped[float] = mapped_column(nullable=False)
    _color_identity: Mapped[str] = mapped_column(nullable=False)
    _produced: Mapped[str] = mapped_column(nullable=True)
    _land: Mapped[bool] = mapped_column(nullable=False)

    _faces: Mapped[List["Face"]] = relationship(back_populates="_card")

    def __repr__(self):
        return '<Card %r>' % self._name
    
    #setters and getters
    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name
    @name.setter
    def name(self, value:str):
        self._name = value

    @property
    def usd(self) -> float:
        return self._usd
    @usd.setter
    def usd(self, value:float):
        self._usd = value

    @property
    def eur(self) -> float:
        return self._eur
    @eur.setter
    def eur(self, value:float):
        self._eur = value

    @property
    def color_identity(self) -> str:
        return self._color_identity
    @color_identity.setter
    def color_identity(self, value:str):
        self._color_identity = value

    @property
    def produced(self) -> str:
        return self._produced
    @produced.setter
    def produced(self, value:str):
        self._produced = value

    @property
    def land(self) -> bool:
        return self._land
    @land.setter
    def land(self, value:bool):
        self._land = value

    @property
    def faces(self) -> Mapped[List["Face"]]:
        return self._faces
    @faces.setter
    def faces(self, value:Mapped[List["Face"]]):
        self._faces = value

    #scrython parsing functions
    
    def check_if_land(self, sco):
        has_land = False
        no_cast = True
        for face in self.faces:
            if isinstance(face, LandFace):
                has_land = True
            elif face.cost != '':
                no_cast = False
        if has_land and no_cast:
            return True
        else:
            return False


    def check_for_produced(self, sco):
        try:
            produced = sco['produced_mana']
            self.produced = "".join(produced)
        except KeyError:
            pass


    def list_faces(self, sco):
        output = []
        try:
            faces = sco['card_faces']
            for face in faces:
                output.append(self.parse_face(face))
        except KeyError:
            output.append(self.parse_face(sco))
        return output



    def parse_face(self, sco):
        if "Land" in sco['type_line'].split(" "):
            land = LandFace()
            land.parse_land_object(sco)
            return land
        else:
            spell = SpellFace()
            spell.parse_spell_object(sco)
            return spell



    def parse_scrython_object(self, sco):
        self.name = sco['name']
        self.color_identity = ''.join(sco['color_identity'])
        self.usd = sco['prices']['usd']
        self.eur = sco['prices']['eur']
        self.check_for_produced(sco)

        self.faces = self.list_faces(sco)
        self.land = self.check_if_land(sco)




