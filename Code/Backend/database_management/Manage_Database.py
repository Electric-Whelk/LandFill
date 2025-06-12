from AppFactory import create_app
from database_management.fillscripts.FormatList import all_formats
from database_management.fillscripts.GamesList import all_games
from database_management.fillscripts.TestCards import test_cards
from DBManager import DBManager
from Extensions import db
from sqlalchemy import MetaData

app = create_app()

with app.app_context():
    engine = db.engine
    metadata = MetaData()
    metadata.reflect(bind=engine)
    man = DBManager(db, app, engine, metadata)


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
        clear = True,
        mass_insert = False,
        source = test_cards,
        parse_legality = True,
        list_unknown_legalities = True
    )