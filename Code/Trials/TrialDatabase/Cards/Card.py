import re

from operator import truediv
from Cards.Face import Face
#from Cards.SpellFace import SpellFace
#from Cards.LandFace import LandFace
from Configure_DB import Base
from Other_Tables.Cycles import Cycle
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing import List

from Other_Tables.Cycles import Cycle


class Card(Base):
    __tablename__ = 'cards'

    _id: Mapped[int] = mapped_column(primary_key=True)
    _name: Mapped[str] = mapped_column(unique=True, nullable=False)
    _usd: Mapped[float] = mapped_column(nullable=True)
    _eur: Mapped[float] = mapped_column(nullable=True)
    _color_identity: Mapped[str] = mapped_column(nullable=False)
    _produced: Mapped[str] = mapped_column(nullable=True)
    _land: Mapped[bool] = mapped_column(nullable=False)
    _layout: Mapped[str] = mapped_column(nullable=True)
    _cycle_id: Mapped[int] = mapped_column(ForeignKey("cycles._id"), nullable=True)

    _faces: Mapped[List["Face"]] = relationship(back_populates="_card")
    _cycle: Mapped["Cycle"] = relationship(back_populates="_card")

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

    @property
    def layout(self) -> Mapped[str]:
        return self._layout
    @layout.setter
    def layout(self, value:Mapped[str]):
        self._layout = value

    @property
    def cycle(self) -> Mapped["Cycle"]:
        return self._cycle
    @cycle.setter
    def cycle(self, value:Mapped["Cycle"]):
        self._cycle = value

    @property
    def cycle_id(self) -> Mapped[int]:
        return self._cycle_id
    @cycle_id.setter
    def cycle_id(self, value:Mapped[int]):
        self._cycle_id = value


    #scrython parsing functions
    
    def check_if_land(self, sco):
        for face in self.faces:
            if face.playable and not face.land:
                return False
        return True


    def check_for_produced(self, sco):
        try:
            produced = sco['produced_mana']
            self.produced = "".join(produced)
        except KeyError:
            pass

    def determine_cycle_from_session(self, session):
        all_cycles = session.query(Cycle).all()
        for cycle in all_cycles:
            if self.cycle is not None:
                break
            regex = cycle.regex
            for face in self.faces:
                test_face = face.text.replace("\n", " ")
                l_test_face = len(test_face)
                matched = re.search(regex, test_face)
                if matched is not None:
                    span = matched.span()
                    if span[0] == 0 and span[1] == l_test_face:
                        print("")
                        print(self.name)
                        print("")
                        self.cycle_id = cycle.id


    def determine_face_playability(self):
        if self.layout == 'transform' or self.layout == 'flip':
            self.faces[0].playable = True
            self.faces[1].playable = False
        else:
            for face in self.faces:
                face.playable = True


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
        face = Face()
        face.parse_face_object(sco)
        return face


    def parse_scrython_object(self, sco):
        self.name = sco['name']
        self.color_identity = ''.join(sco['color_identity'])
        self.usd = sco['prices']['usd']
        self.eur = sco['prices']['eur']
        self.layout = sco['layout']
        self.check_for_produced(sco)

        self.faces = self.list_faces(sco)
        self.determine_face_playability()

        self.land = self.check_if_land(sco)




