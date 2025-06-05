import scrython
from Cards.Card import Card
from Cards.SpellFace import SpellFace
from Cards.TestCards import test_cards
from Configure_DB import Base
from Configure_DB import engine
from Configure_DB import session
from sqlalchemy import select
from sqlalchemy import text
from typing import List

def one_card_search(term):
    outp = scrython.cards.Search(q=term).data()[0]
    print(outp['name'] + "  " + str(outp))
    return outp

def control_panel(session, cards,
          destroy:bool=False,
          mass_insert:bool=False,
          scalars_statement=None):
    if destroy:
        sesh.execute(text('drop table if exists cards'))
        sesh.execute(text('drop table if exists spell_faces'))
        sesh.execute(text('drop table if exists land_faces'))
        sesh.execute(text('drop table if exists faces'))
    if mass_insert:
        Base.metadata.create_all(bind=engine)
        sesh.add_all(cards)
    if scalars_statement is not None:
        result = sesh.scalars(scalars_statement)
        print("Results:")
        for r in result:
            print(r)
        print("/Results")



allcards = []
count = 0

for obj in test_cards:
    count += 1
    try:
        c = Card()
        c.parse_scrython_object(obj)
        allcards.append(c)
    except Exception as e:
        print("Error for card " + str(count) + ": " + str(e))

with session as sesh:
    #scalars:
        #select
        #join: select(SpellFace).join(SpellFace._card).where(Card._usd == 10.68)

    control_panel(sesh, allcards,
                  destroy=False,
                  mass_insert=False,
                  scalars_statement = select(SpellFace).join(SpellFace._card).where(Card._id == 4))
    sesh.commit()

