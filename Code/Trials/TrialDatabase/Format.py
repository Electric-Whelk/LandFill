from Configure_DB import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Format(Base):
    __tablename__ = 'formats'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True)
    singleton: Mapped[bool] = mapped_column(nullable=False)
    min: Mapped[int] = mapped_column(nullable=False)
    max: Mapped[int] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return self.name

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "singleton": self.singleton,
            "min": self.min,
            "max": self.max,
        }



