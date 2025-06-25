import re

from ColorPie import ColorPie
from database_management.models.Cycle import Cycle
from database_management.models.Face import Face
from database_management.models.Format import Format
from database_management.models.Game import Game
from database_management.models.Intermediates import Banned, Restricted, Legal, GameCards
from Extensions import db
from functools import cached_property
from sqlalchemy import select
from typing import Dict, List

#(.*): Mapped\[(.*)\] = mapped_column\((.*)\)

class Card(db.Model):
    __tablename__ = 'cards'
    _id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String, nullable=False, unique=True)
    _cmc = db.Column(db.Integer, nullable=False)
    _usd = db.Column(db.String, nullable=False)
    _eur = db.Column(db.String, nullable=False)
    _color_identity = db.Column(db.String, nullable=False)
    _produced = db.Column(db.String, nullable=False)
    _overall_land = db.Column(db.Boolean, nullable=False)
    _layout = db.Column(db.String, nullable=False)
    _game_changer = db.Column(db.Boolean, nullable=False)
    _silver_bordered = db.Column(db.Boolean, nullable=False)
    _cycle_id = db.Column(db.Integer, db.ForeignKey('cycles._id'), nullable=False)
    _last_printing = db.Column(db.String, nullable=False)

    _cycle = db.relationship('Cycle', back_populates='_cards')

    _faces = db.relationship('Face',
                             back_populates='_card',
                             passive_deletes=True)

    _banned = db.relationship('Format',
                              secondary=Banned.__table__,
                              back_populates='_banned',
                              passive_deletes=True)
    _restricted = db.relationship('Format',
                                  secondary=Restricted.__table__,
                                  back_populates='_restricted',
                                  passive_deletes=True)
    _legal = db.relationship('Format',
                             secondary=Legal.__table__,
                             back_populates='_legal',
                             passive_deletes=True)

    _games = db.relationship('Game',
                             secondary=GameCards.__table__,
                             back_populates='_cards',
                             passive_deletes=True)

    def __init__(self):
        self._banned = []
        self._restricted = []
        self._legal = []
        self._games = []
    
    #getters and setters
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
    def overall_land(self) -> bool:
        return self._overall_land
    @overall_land.setter
    def overall_land(self, value:bool):
        self._overall_land = value

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

    @property
    def banned(self) -> List["Format"]:
        return self._banned
    @banned.setter
    def banned(self, value:List["Format"]):
        self._banned = value

    @property
    def restricted(self) -> List["Format"]:
        return self._restricted
    @restricted.setter
    def restricted(self, value:List["Format"]):
        self._restricted = value

    @property
    def legal(self) -> List["Format"]:
        return self._legal
    @legal.setter
    def legal(self, value:List["Format"]):
        self._legal = value

    @property
    def games(self) -> List["Game"]:
        return self._games
    @games.setter
    def games(self, value:List["Game"]):
        self._games = value

    @property
    def last_printing(self) -> str:
        return self._last_printing
    @last_printing.setter
    def last_printing(self, value:str):
        self._last_printing = value

    @property
    def cycle_id(self) -> int:
        return self._cycle_id
    @cycle_id.setter
    def cycle_id(self, value:int):
        self._cycle_id = value

    @property
    def cycle(self) -> Cycle:
        return self._cycle
    @cycle.setter
    def cycle(self, value:Cycle):
        self._cycle = value

    #cached properties
    @cached_property
    def produced_score(self) -> ColorPie:
        if not self.overall_land:
            return 0

        l_text = self.check_searched_lands()
        l_produced = list(self.produced)
        pie = ColorPie()
        pie.parse_colors(l_produced)
        pie.parse_lands(l_text)
        pie.parse_lands(self.subtypes)
        return pie


    @cached_property
    def parsed_types(self) -> Dict[str, List[str]]:
        supertypes = []
        types = []
        subtypes = []

        for face in self.faces:
            supertypes.extend(face.supertypes)
            types.extend(face.cardtypes)
            subtypes.extend(face.subtypes)

        return {"supertypes": supertypes, "cardtypes": types, "subtypes": subtypes}

    @cached_property
    def typed(self) -> bool:
        if "Land" not in self.cardtypes:
            return False
        land_types = ["Plains",
                      "Island",
                      "Swamp",
                      "Mountain",
                      "Forest"]
        for type in land_types:
            if type in self.subtypes:
                return True
        return False

    @cached_property
    def text(self) -> str:
        text = ""
        for face in self.faces:
            text += face.text
        return text


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





    #parsing functions
    def add_face_manually(self, sco):
        self.faces.append(self.parse_face(sco))
        self.determine_face_playability()
        self.overall_land = self.check_if_land()

    def check_for_produced(self, sco):
        try:
            produced = sco["produced_mana"]
            self.produced = "".join(produced)
        except Exception:
            self.produced = "none"

    def check_searched_lands(self):
        if not self.cycle.fetch:
            return []
        words = self.text.split()
        return words
            
    def check_if_land(self):
        for face in self.faces:
            if face.playable and not face.land:
                return False
        return True

    def determine_cycle(self):
        self.reset_cycle()
        check_synergy = True
        for face in self.faces:
            if "Land" not in face.cardtypes:
                check_synergy = False

        edge_cases = ["Wastes",
                      "Snow-Covered Wastes",
                      "Coastal Tower"]
        if check_synergy and self.name in edge_cases:
            self.determine_cycle_edge_case()
            check_synergy = False

        if check_synergy:
            if len(self.faces) == 2:
                cycle_synergy = "Dual-Faced"
            elif "Snow" in self.supertypes:
                cycle_synergy = "Snow"
            elif "Artifact" in self.cardtypes:
                cycle_synergy = "Artifact"
            elif "Gate" in self.subtypes:
                cycle_synergy = "Gate"
            elif "Desert" in self.subtypes:
                cycle_synergy = "Desert"
            elif "Town" in self.subtypes:
                cycle_synergy = "Town"
            else:
                cycle_synergy = "None"


            self.determine_cycle_regex(syn=cycle_synergy, typed=self.typed)




    def determine_cycle_regex(self, syn=None, typed=None):
        result = db.session.query(Cycle)
        result = result.filter(Cycle._synergy == syn)
        result = result.filter(Cycle._typed == typed).all()


        #statement = select(Cycle).where(Cycle._synergy == syn and Cycle._name != "misc")
        #result = db.session.scalars(statement)
        for c in result:
            regex = c.regex
            for face in self.faces:
                test_face = face.text.replace("\n", " ")
                l_test_face = len(test_face)
                matched = re.search(regex, test_face)
                if matched is not None:
                    span = matched.span()
                    if span[0] == 0 and span[1] == l_test_face:
                        print("Adding " + self.name + " to cycle " + c.name)
                        self.cycle = c


    def determine_cycle_edge_case(self):
        match self.name:
            case "Wastes":
                self.cycle = db.session.query(Cycle).filter(Cycle._name == "Basic Lands").first()
            case "Snow-Covered Wastes":
                self.cycle = db.session.query(Cycle).filter(Cycle._name == "Snow Basic Lands").first()
            case "Coastal Tower":
                self.cycle = db.session.query(Cycle).filter(Cycle._name == "Vanilla Dual Lands").first()


    def determine_face_playability(self):
        if self.layout == 'transform' or self.layout == 'flip':
            self.faces[0].playable = True
            self.faces[1].playable = False
        else:
            for face in self.faces:
                face.playable = True

    def determine_games_from_object(self, sco):
        games_list = sco['games']
        games_table = db.session.query(Game).all()
        for game in games_table:
            if game.scryfall_name in games_list:
                self.games.append(game)


    def determine_legality_from_object(self, sco):
        formats = db.session.query(Format).all()
        for format in formats:
            try:
                status = sco['legalities'][format.scryfall_name]
            except KeyError:
                status = format.display_name
            self.set_format_association(format, status)

    def handle_price(self, object):
        try:
            if object is not None:
                return int(float(object) * 100)
            else:
                return -1
        except KeyError:
            return -1
        
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

        self.usd = self.handle_price(sco['prices']['usd'])
        self.eur = self.handle_price(sco['prices']['eur'])
        self.layout = sco['layout']
        self.game_changer = sco['game_changer']
        self.silver_bordered = sco['set_type'] == 'funny'
        self.last_printing = sco['set_name']
        self.cycle_id = 1
        self.check_for_produced(sco)

        self.faces = self.list_faces(sco)
        self.determine_face_playability()

        self.overall_land = self.check_if_land()

    def reset_cycle(self):
        statement = select(Cycle).where(Cycle._id == 1)
        result = db.session.scalars(statement).one()
        self.cycle = result

    def set_format_association(self, format, status):
        match status:
            case 'not_legal':
                self.banned.append(format)
            case 'banned':
                self.banned.append(format)
            case 'legal':
                self.legal.append(format)
            case 'restricted':
                self.restricted.append(format)
            case 'Limited':
                self.legal.append(format)
            case _:
                raise Exception(f"{status} not understood by format association function")


    #app interaction functions
    def to_JSON(self):
        output = {
            "id": self.id,
            "name": self.name,
            "cmc": self.cmc,
            "usd": self.usd,
            "eur": self.eur,
            "color_identity": self.color_identity,
            "produced": self.produced,
            "overall_land": self.overall_land,
            "layout": self.layout,
            "game_changer": self.game_changer,
            "silver_bordered": self.silver_bordered,
            "cycle_id": self.cycle_id,
            "last_printing": self.last_printing,
            "typed": self.typed,
            "cardtypes": self.cardtypes,
            "subtypes": self.subtypes,
            "supertypes": self.supertypes,
        }

        i = 0
        for face in self.faces:
            output.update({f"face_{i}": face.to_JSON()})
            i += 1

        return output