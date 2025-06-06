from Cards.Face import Face
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class LandFace(Face):
    __tablename__ = "land_faces"

    _id: Mapped[int] = mapped_column(ForeignKey("faces._id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "land",
    }

    #getters and setters
    @property
    def id(self) -> int:
        return self._id

    #scrython construction functions
    def parse_land_object(self, obj):
        self.parse_face_object(obj)