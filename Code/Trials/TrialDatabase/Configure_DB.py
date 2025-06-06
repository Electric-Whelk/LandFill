from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase

import scrython

engine = create_engine('sqlite:////home/electricwhelk/FinalProject/Code/Trials/TrialDatabase/mtg.db', echo=True)
session = Session(bind=engine)

class Base(DeclarativeBase):
    pass

cycle_regex = {
    "shock_lands":"\(\{T\}: Add \{[WUBRG]\} or \{[WUBRG]\}\.\) As this land enters, you may pay 2 life. If you don't, it enters tapped.",
    "bond_lands":"This land enters tapped unless you have two or more opponents. \{T\}: Add \{[WUBRG]\} or \{[WUBRG]\}."
}
