from unittest.mock import PropertyMock

import scrython

class SCCard:
    def __init__(self, name, cmc, color_identity, price, supertypes, types, subtypes, oracle_text, legality, games, release_date):
        self._name = name
        self._cmc = cmc
        self._identity = color_identity
        self._price = price
        self._supertypes = supertypes
        self._types = types
        self._subtypes = subtypes
        self._oracle_text = oracle_text
        self._legality = legality
        self._games = games
        self._release_date = release_date



    #setters and getters
    @property
    def cmc(self):
        return self._cmc

    @property
    def name(self):
        return self._name

    @property
    def oracle_text(self):
        return self._oracle_text

    @property
    def release_date(self):
        return self._release_date

    @property
    def subtypes(self):
        return self._subtypes

    @property
    def types(self):
        return self._types

    
    #other functions, alphabetized
    def print(self):
        print(self._name)
        print(self._cmc)
        print(self._identity)
        print(self._price)
        print(self._supertypes)
        print(self._types)
        print(self._subtypes)
        print(self._oracle_text)
        print(self._legality)
        print(self._games)
        print(self._release_date)
        





