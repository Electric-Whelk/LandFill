import scrython
from Cards.Card import Card
from Cards.Face import Face
#from Cards.LandFace import LandFace
#from Cards.SpellFace import SpellFace
from Cards.TestCards import test_cards
from Configure_DB import Base
from Configure_DB import engine
from Configure_DB import session
from Other_Tables.AllCycles import all_cycles
from Other_Tables.Cycles import Cycle
from sqlalchemy import select
from sqlalchemy import text
from typing import List

def one_card_search(term):
    outp = scrython.cards.Search(q=term).data()[0]
    print(outp['name'] + "  " + str(outp))
    return outp

def amid(text):
    print("")
    print(text)
    print("")

def clear_table(session, cls):
    #doesn't commit
    result = session.query(cls).all()
    for object in result:
        session.delete(object)


def control_panel(session,
          destroy:bool=False,
          mass_insert:bool=False,
          scalars_statement=None):
    if destroy:
        amid("destroying")
        #clear_table(session, Card)
        #clear_table(session, Face)
        #'"""
        cards = session.query(Card).all()
        faces = session.query(Face).all()
        for card in cards:
            session.delete(card)
        for face in faces:
            session.delete(face)
            #"""

        sesh.commit()
    if mass_insert:
        amid("creating")
        pull_TestCards(session)
        sesh.commit()
    if scalars_statement is not None:
        result = sesh.scalars(scalars_statement)
        print("Results:")
        for r in result:
            print(r)
        print("/Results")

def pull_TestCards(session):
    allcards = []
    count = 0

    amid("beginning")

    for obj in test_cards:
        count += 1
        try:
            c = Card()
            session.add(c)
            c.parse_scrython_object(obj)
            c.determine_cycle_from_session(session)
            allcards.append(c)
        except Exception as e:
            print("Error for card " + str(count) + ": " + str(e))
        session.add_all(allcards)

def rebuild_cycles(session):
    for cycle in all_cycles:
        session.add(cycle)
    session.commit()



with session as sesh:
    Base.metadata.create_all(bind=engine)

    control_panel(sesh,
                  destroy=False,
                  mass_insert=True,
                  scalars_statement = None)

    #rebuild_cycles(sesh)




    #scalars_statement = select(Face).join(Face._card).where(Card._id == 4)

