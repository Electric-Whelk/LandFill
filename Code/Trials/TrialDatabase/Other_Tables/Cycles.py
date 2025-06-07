import re
from Configure_DB import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Cycle(Base):
    __tablename__ = 'cycles'

    _id: Mapped[int] = mapped_column(primary_key=True)
    _name: Mapped[str] = mapped_column(unique=True, nullable=False)
    _regex: Mapped[str] = mapped_column(unique=True, nullable=True)

    _card: Mapped["Card"] = relationship(back_populates="_cycle")

    def __repr__(self):
        return self.name

    #getters and setters
    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value

    @property
    def regex(self):
        return self._regex
    @regex.setter
    def regex(self, value):
        self._regex = value


