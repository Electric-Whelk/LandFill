import unittest

from AppFactory import create_app
from database_management.DBManager import DBManager
from Extensions import db

class UnitTestDB(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)

        self.dbm = DBManager(db, create_app())


    def test_count(self):
        not_funny = self.dbm.count_rows("cards",
                                        condition = "_silver_bordered = 0",
                                        context = True)

        crd = {"not_funny": "_silver_bordered = 0",
                      "adventure": "_layout = 'adventure'"
               }

        for key in crd:
            value = crd[key]
            crd[key] = self.dbm.count_rows("cards",
                                           condition = value,
                                           context = True)



        self.assertEqual(crd["not_funny"], 29266)
        self.assertEqual(crd["adventure"], 122)

    def cmc_gradient(self):
        #corresponds respectively to the number of printed cards of cmc 0, 1, 2, 3, 4, 5 and greater
        #used in assert testing for a mass download
        #will also need to be incorporated into any scheduled update routine, but for now can just
        #be declared.
        return [1299, 2932, 6198, 7104, 5620, 3549, 3165]

