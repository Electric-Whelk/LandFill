from AppFactory import create_app
from database.tables.Card import Card
from database.testing.TestCards import test_cards
from Extensions import db

app = create_app()

with app.app_context():

    for sco in test_cards:
        new_card = Card()
        new_card.parse_scrython_object(sco)
        db.session.add(new_card)
        db.session.commit()

