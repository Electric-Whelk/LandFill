from Cards.Card import Card
from Configure_DB import Base
from Configure_DB import engine
from Configure_DB import session
from Other_Tables.AllCycles import all_cycles
from sqlalchemy import select


def add_cycles(cycles, session,
               add_to_table=False,
               add_to_cards=False):

    if add_to_table:
        session.add_all(cycles)
        session.commit()
    if add_to_cards:
        ##add a clause that does not reset the cycles on cards that have them already?
        statement = select(Card).where(Card._land == True)
        lands = session.scalars(statement)
        for land in lands:
            land.determine_cycle_from_session(session)
        session.commit()


with session as session:
    add_cycles(all_cycles, session,
               add_to_table=True,
               add_to_cards=True)


