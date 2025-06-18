import unittest
import random

from AppFactory import create_app
from database_management.DBManager import DBManager
from Extensions import db
from sqlalchemy import MetaData

class UnitTestDB(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)

        self.app = create_app()

        with self.app.app_context():
            engine = db.engine
            metadata = MetaData()
            metadata.reflect(bind=engine)
            self.dbm = DBManager(db, self.app, engine, metadata)




    def test_multiple_faces(self):
        with self.app.app_context():

            i = 1
            while i <= 500:
                #max = 29822

                #id = 26042
                id = random.randrange(1, 29823)
                i += 1
                card = self.dbm.key_lookup(id, "cards", "id")
                faces = self.dbm.key_lookup(card.id, "faces", "card_id",
                                            expect_single=False)

                print(f"Testing {card.name}...")

                listfaces = list(faces)
                facecount = len(listfaces)
                silver = card.silver_bordered

                #non-unset cards should always have 2 or fewer faces
                if not silver:
                    self.assertLessEqual(facecount, 2, f"improper facecount for {card.name}")

                #two faces never have the same text
                if facecount == 2:
                    self.assertNotEqual(listfaces[0], listfaces[1], f"unequal faces for {card.name}")




