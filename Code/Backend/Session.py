from unittest.mock import PropertyMock

import scrython

class Session:
    def __init__(self, input):
        #factors that are determined once at the start and are not changed as the program iterates
        self._non_lands = input.get("nonLands")
        self._format = input.get("Format")
        self._colors = self.determine_colors()
        self._land_slots = self.determine_land_slots()

    #calculating functions used in the input
    def determine_colors(self):
        return 0

    def determine_land_slots(self):
        return 0




    #setter and getter functions
    @property
    def non_lands(self):
        return self._non_lands

    @non_lands.setter
    def non_lands(self, value):
        self._non_lands = value