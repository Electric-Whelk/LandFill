from Cards.Face import Face
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class SpellFace(Face):
    __tablename__ = "spell_faces"

    _id: Mapped[int] = mapped_column(ForeignKey("faces._id"), primary_key=True)
    _cost: Mapped[str] = mapped_column(nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "spell",
    }

    #getters and setters
    @property
    def id(self) -> int:
        return self._id

    @property
    def cost(self) -> str:
        return self._cost
    @cost.setter
    def cost(self, value: str):
        self._cost = value

    #setup functions
    def parse_mana_cost(self, cost):
        """
        Back when I was thinking of this as having individual values. I think it'd be easier to not
        cost = list(cost)
        dict = {'W': 0, 'U': 0, 'B': 0, 'R': 0, 'G': 0, 'C':0}
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
        """
        return cost.replace("{","").replace("}","")


    def parse_spell_object(self, obj):
        self.parse_face_object(obj)
        self.cost = self.parse_mana_cost(obj["mana_cost"])

