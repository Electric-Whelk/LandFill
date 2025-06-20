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
        #with self.app.app_context():

        i = 1
        while i <= 500:
            #max = 29822

            #id = 26042
            id = random.randrange(1, 29823)
            i += 1
            card = self.dbm.key_lookup(id, "cards", "id",
                                       context=True)
            faces = self.dbm.key_lookup(card.id, "faces", "card_id",
                                        expect_single=False, context=True)

            print(f"Testing {card.name}...")

            facecount = len(faces)
            silver = card.silver_bordered

            #non-unset cards should always have 2 or fewer faces
            if not silver:
                self.assertLessEqual(facecount, 2, f"improper facecount for {card.name}")

            #two faces never have the same text
            if facecount == 2:
                self.assertNotEqual(faces[0].text, faces[1].text, f"unequal faces for {card.name}")


    def test_cycles(self):
        expected = {
            #sure
            "Shock Lands": 10,
            "Check Lands": 10,
            "Reveal Lands": 10,
            "Filter Lands": 10,
            "Bond Lands": 10,
            "OG Dual Lands": 10,
            "Horizon Lands": 6,
            "Verge Lands": 10,
            "OG Filter Lands": 10,
            "Tainted Lands": 4,
            "Tango Lands": 5,
            "Fast Lands": 10,
            "Slow Lands": 10,
            "Pain Lands": 10,
            "Unlucky Lands": 10,
            "Exert Lands": 10,
            "Exert Depletion Lands": 5,
            "Fetch Lands": 10,
            "Snow Dual Lands": 10,
            "Typed Dual Lands": 10,
            "Vanilla Dual Lands": 15,
            "Triomes": 10,
            "Surveil Lands": 10,
            "Cycling Lands": 5,

            "Locales": 5,
            "Landscapes": 10,
            "Panoramas": 5,
            "Mirage Fetches": 5,

            "Time Spiral Storage Lands": 5,
            "Fallen Empires Storage Lands": 5,
            "Masque Storage Lands": 5,

            "Snow Basic Lands": 6,
            "Basic Lands": 6,
            "Dual Faced Lands": 10,
            "Thriving Gates": 5,
            "Thriving Lands": 5,
            "Bounce Lands": 10,
            "Visions Bounce Lands": 5,
            "Invasion Sac Lands": 5,
            "Vivid Lands": 5,
            "Gain Lands": 15,
            "Tri-Color Taplands": 10,
            "Lairs": 5,
            "Masque Depletion Lands": 5,
            "Home Lands": 5,
            "Junction Deserts": 10,
            "Guildgates": 10,
            "Towns": 10,
            "Artifact Lands": 5,
            "Tapped Pain Lands": 5,
            "Monocolor Sac Lands": 5,
            "Tricolor Sac Lands": 5

        }
        with self.app.app_context():

            cycles = self.dbm.all_entries("cycles", context=False)
            errors = []
            for cycle in cycles:
                if cycle.name != "misc":
                    card_count = len(cycle.cards)
                    name = cycle.name
                    exp = expected[name]
                    if card_count != exp:
                        errors.append(f"id {cycle.id}: Expected {exp} {name} but got {card_count}")

            for error in errors:
                print(error)

            self.assertEqual(len(errors), 0, "\nErrors listed above.")







