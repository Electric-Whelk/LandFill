from unittest.mock import PropertyMock

import scrython

class Session:
    def __init__(self, input):
        self._non_lands = input.get("nonLands")
        self._format = "EDH"
        self._colors = self.determine_colors()

    #calculating functions used in the input
    def determine_colors(self):




    #setter and getter functions
    @property
    def non_lands(self):
        return self._non_lands

    @non_lands.setter
    def non_lands(self, value):
        self._non_lands = value