from AppFactory import create_app
#from database_management.fillscripts.AllCards import all_cards
from database_management.fillscripts.CycleList import all_cycles
from database_management.fillscripts.FormatList import all_formats
from database_management.fillscripts.GamesList import all_games
from database_management.fillscripts.TestCards import test_cards
from DBManager import DBManager
from Extensions import db
from sqlalchemy import MetaData, text

app = create_app()

with app.app_context():
    engine = db.engine
    metadata = MetaData()
    metadata.reflect(bind=engine)
    man = DBManager(db, app, engine, metadata)


    man.manage_cycles(
                        drop=False,
                        clear=False,
                        mass_insert=True,
                        source=all_cycles,
                        reset_cards=False

    )

    man.manage_games(
                        drop=False,
                        clear=False,
                        mass_insert=False,
                        source=all_games,
    )

    man.manage_formats(
                       drop=False,
                       clear=False,
                       mass_insert=False,
                       source=all_formats,
    )

    man.manage_cards(
        drop = False,
        clear = False,
        mass_insert = False,
        source = 0,
        parse_legality = False,
        list_unknown_legalities = False,
        set_lands = True,
        only_lands = True
    )

    man.get_card_information(
        run=False,
        source=test_cards
    )





