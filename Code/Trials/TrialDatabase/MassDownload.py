import time
import scrython

from Cards.Card import Card
from Cards.Face import Face
from Configure_DB import Base
from Configure_DB import engine
from Configure_DB import session
from Other_Tables.AllCycles import all_cycles
from Other_Tables.Cycles import Cycle
from sqlalchemy import select
from sqlalchemy import text
from TestRun import amid
from TestRun import control_panel
from typing import List

def mass_lookup(search_term, session):
    more = True
    page = 1
    while more:
        result = scrython.cards.Search(q=search_term, page=page)
        for card in result.data():
            output = []
            tmp = card
            output.append(tmp)
            control_panel(session, output,
                          destroy=False,
                          mass_insert=True,
                          scalars_statement=None,
                          include_cycles=False)
        more = result.has_more()
        page += 1
        time.sleep(0.5)

#total paper cards: 29868
##lands: type:land (game:paper) cmc=0  expect 1020
#nonlands: (-type:land or cmc>0) and (game:paper) expect 28848

#bottom of the nonlands: -type:land and cmc=0 and game:paper

#(when you reset you may want to edit so that the final fantasy adventure lands come with nonlands)
#cmc 0 = 1299<
#cmc 1 = 2932<
#cmc 2 = 6198<
#cmc 3 = 7104<
#cmc 4 = 5620<
#cmc 5 = 3549<
#cmc > 5 = 3165

#cmc=2 and game:paper

#with session as session:
    #Base.metadata.create_all(bind=engine)
    #search_term = ("cmc>5 and game:paper")
    #mass_lookup(search_term, session)
