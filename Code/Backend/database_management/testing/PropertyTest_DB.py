from AppFactory import create_app

from database_management.DBManager import DBManager
from Extensions import db
from sqlalchemy import MetaData, text

app = create_app()

def test_multiple_faces(id, man):
    card = man.key_lookup(id, "cards", "id")
    faces = man.key_lookup(card.id, "faces", "card_id", expect_single = False)

    """   if not card.silver_bordered:
        assert len(list(faces)) <= 2

    """
    print(len(list(faces)))


with app.app_context():
    engine = db.engine
    metadata = MetaData()
    metadata.reflect(bind=engine)
    man = DBManager(db, app, engine, metadata)

    test_multiple_faces(1, man)



