from database.tables.Face import Face
from Extensions import db
from typing import List


#(.*): Mapped\[(.*)\] = mapped_column\((.*)\)

class Card(db.Model):
    __tablename__ = 'cards'
    _id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String, nullable=False)
    _cmc = db.Column(db.String, nullable=False)
    _usd = db.Column(db.String, nullable=False)
    _eur = db.Column(db.String, nullable=False)
    _color_identity = db.Column(db.String, nullable=False)
    _produced = db.Column(db.String, nullable=False)
    _overall_land = db.Column(db.Boolean, nullable=False)
    _layout = db.Column(db.String, nullable=False)
    _game_changer = db.Column(db.Boolean, nullable=False)
    _silver_bordered = db.Column(db.Boolean, nullable=False)

    _faces = db.relationship('Face', back_populates='_card')
    
    #getters and setters
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
    
    #parsing functions
    def check_for_produced(self, sco):
        try:
            produced = sco["produced_mana"]
            self.produced = "".join(produced)
        except Exception:
            self.produced = "none"
            
    def check_if_land(self):
        for face in self.faces:
            if face.playable and not face.land:
                return False
        return True
            
    def determine_face_playability(self):
        if self.layout == 'transform' or self.layout == 'flip':
            self.faces[0].playable = True
            self.faces[1].playable = False
        else:
            for face in self.faces:
                face.playable = True
    
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

        self.overall_land = self.check_if_land()

