from AppFactory import create_app
from database_management.testing.TestCards import test_cards
from DBManager import DBManager
from Extensions import db
from sqlalchemy import MetaData

app = create_app()

with app.app_context():
    engine = db.engine
    metadata = MetaData()
    metadata.reflect(bind=engine)
    man = DBManager(db, app, engine, metadata)


    man.reset("cards")