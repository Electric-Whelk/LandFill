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
    _name: Mapped[str] = mapped_column(nullable=False)
    _cmc: Mapped[int] = mapped_column(nullable=False)
    _usd: Mapped[float] = mapped_column(nullable=False)
    _eur: Mapped[float] = mapped_column(nullable=False)
    _color_identity: Mapped[str] = mapped_column(nullable=False)
    _produced: Mapped[str] = mapped_column(nullable=False)
    _land: Mapped[bool] = mapped_column(nullable=False)
    _layout: Mapped[str] = mapped_column(nullable=False)
    _game_changer: Mapped[bool] = mapped_column(nullable=False)
    _cycle_id: Mapped[int] = mapped_column(ForeignKey("cycles._id"), nullable=True)
    _silver_bordered: Mapped[bool] = mapped_column(nullable=False)

    _standard: Mapped[str] = mapped_column(nullable=False)
    _future: Mapped[str] = mapped_column(nullable=False)
    _historic: Mapped[str] = mapped_column(nullable=False)
    _timeless: Mapped[str] = mapped_column(nullable=False)
    _gladiator: Mapped[str] = mapped_column(nullable=False)
    _pioneer: Mapped[str] = mapped_column(nullable=False)
    _explorer: Mapped[str] = mapped_column(nullable=False)
    _modern: Mapped[str] = mapped_column(nullable=False)
    _legacy: Mapped[str] = mapped_column(nullable=False)
    _pauper: Mapped[str] = mapped_column(nullable=False)
    _vintage: Mapped[str] = mapped_column(nullable=False)
    _penny: Mapped[str] = mapped_column(nullable=False)
    _commander: Mapped[str] = mapped_column(nullable=False)
    _oathbreaker: Mapped[str] = mapped_column(nullable=False)
    _standardbrawl: Mapped[str] = mapped_column(nullable=False)
    _brawl: Mapped[str] = mapped_column(nullable=False)
    _alchemy: Mapped[str] = mapped_column(nullable=False)
    _paupercommander: Mapped[str] = mapped_column(nullable=False)
    _duel: Mapped[str] = mapped_column(nullable=False)
    _oldschool: Mapped[str] = mapped_column(nullable=False)
    _premodern: Mapped[str] = mapped_column(nullable=False)
    _predh: Mapped[str] = mapped_column(nullable=False)


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
    def cmc(self) -> int:
        return self._cmc
    @cmc.setter
    def cmc(self, value:int):
        self._cmc = value

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
    def faces(self) -> List["Face"]:
        return self._faces
    @faces.setter
    def faces(self, value:List["Face"]):
        self._faces = value

    @property
    def layout(self) -> str:
        return self._layout
    @layout.setter
    def layout(self, value:str):
        self._layout = value

    @property
    def cycle(self) -> "Cycle":
        return self._cycle
    @cycle.setter
    def cycle(self, value:"Cycle"):
        self._cycle = value

    @property
    def cycle_id(self) -> int:
        return self._cycle_id
    @cycle_id.setter
    def cycle_id(self, value:int):
        self._cycle_id = value

    @property
    def game_changer(self) -> bool:
        return self._game_changer
    @game_changer.setter
    def game_changer(self, value:bool):
        self._game_changer = value

    @property
    def silver_bordered(self) -> bool:
        return self._silver_bordered
    @silver_bordered.setter
    def silver_bordered(self, value:bool):
        self._silver_bordered = value


    #scrython parsing functions
    
    def check_if_land(self, sco):
        for face in self.faces:
            if face.playable and not face.land:
                return False
        return True


    def check_for_produced(self, sco):
        try:
            produced = sco["produced_mana"]
            self.produced = "".join(produced)
        except Exception:
            self.produced = "none"

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

    def determine_legalities(self, leg):
        """
        for format in leg:
            if leg.get(format) == 'not_legal':
                leg[format] = False
            elif leg.get(format) == 'legal':
                leg[format] = True
            else:
                raise Exception("Legality of " + self.name + " in format " + format + " is unknown")
        print("Standard: " + str(leg["standard"]))
        """
        self._standard = leg["standard"]
        self._future = leg["future"]
        self._historic = leg["historic"]
        self._timeless = leg["timeless"]
        self._gladiator = leg["gladiator"]
        self._pioneer = leg["pioneer"]
        self._explorer = leg["explorer"]
        self._modern = leg["modern"]
        self._legacy = leg["legacy"]
        self._pauper = leg["pauper"]
        self._vintage = leg["vintage"]
        self._penny = leg["penny"]
        self._commander = leg["commander"]
        self._oathbreaker = leg["oathbreaker"]
        self._standardbrawl = leg["standardbrawl"]
        self._brawl = leg["brawl"]
        self._alchemy = leg["alchemy"]
        self._paupercommander = leg["paupercommander"]
        self._duel = leg["duel"]
        self._oldschool = leg["oldschool"]
        self._premodern = leg["premodern"]
        self._predh = leg["predh"]

    def handle_nullable(self, object, value_if_null):
        try:
            if object is not None:
                return object
            else:
                return value_if_null
        except KeyError:
            return value_if_null

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
        self.cmc = sco['cmc']
        self.usd = self.handle_nullable(sco['prices']['usd'], -1)
        self.eur = self.handle_nullable(sco['prices']['eur'], -1)
        self.layout = sco['layout']
        self.game_changer = sco['game_changer']
        self.silver_bordered = sco['set_type'] == 'funny'
        self.cycle_id = 0
        self.check_for_produced(sco)

        self.faces = self.list_faces(sco)
        self.determine_face_playability()

        self.land = self.check_if_land(sco)

        self.determine_legalities(sco['legalities'])




