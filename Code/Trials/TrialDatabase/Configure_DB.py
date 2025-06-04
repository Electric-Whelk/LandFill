from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase

import scrython

engine = create_engine('sqlite:///mtg.db', echo=True)
session = Session(bind=engine)

class Base(DeclarativeBase):
    pass

