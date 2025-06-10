import re
from Cards.Card import Card
from Configure_DB import Base
from sqlalchemy import select
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing import List

class Cycle(Base):
    __tablename__ = 'cycles'

    _id: Mapped[int] = mapped_column(primary_key=True)
    _name: Mapped[str] = mapped_column(unique=True, nullable=False)
    _regex: Mapped[str] = mapped_column(unique=True, nullable=True)

    _cards: Mapped[List["Card"]] = relationship(back_populates="_cycle")

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

    @property
    def cards(self) -> List[Card]:
        return self._cards





    #other methods (alphabetized)
    def assign_lands(self, session):
        lands_lookup = select(Card).where(Card._land == True)
        all_lands = session.execute(lands_lookup).all()
        for land in all_lands:
            if land.cycle_id != 0:
                for face in land.faces:
                    test_face = face.text.replace("\n", " ")
                    l_test_face = len(test_face)
                    matched = re.search(self.regex, test_face)
                    if matched is not None:
                        span = matched.span()
                        if span[0] == 0 and span[1] == l_test_face:
                            print("Adding " + self.name + " to cycle " + self.name)
                            land.cycle_id = self.id



        """    def determine_cycle_from_session(self, session):
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
                                print("Adding " + self.name + " to cycle " + cycle.name)
                                self.cycle_id = cycle.id
        """

    def lands_to_json(self):
        cards_json = [x.to_json() for x in self.cards]
        return {
            "id": self.id,
            "name": self.name,
            "cards": cards_json
        }

    def query_lands(self, session):
        statement = select(Card).where(Card._cycle_id == self.id)
        return list(session.scalars(statement))




