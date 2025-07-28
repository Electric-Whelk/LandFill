import os
import joblib
import pickle

from simulation_objects.Timer import functimer_once


class LandPermutationCache:
    @functimer_once
    def __init__(self, filename="permutation_cache.pkl"):
        self.filename = filename
        try:
            with open(filename, "rb") as f:
                self.cache = pickle.load(f)
                print(f"Loaded cache of length {len(self.cache)}")
        except FileNotFoundError:
            self.cache = {}

        self.setcount = 0
        self.getcount = 0

    def compare(self):
        print(f"misses: {self.setcount} hits: {self.getcount}")
        self.setcount = self.getcount = 0

    def hit(self):
        self.getcount += 1

    def miss(self):
        self.setcount += 1

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache[key] = value

    def save(self):
        temp_filename = self.filename + ".tmp"
        with open(temp_filename, "wb") as f:
            pickle.dump(self.cache, f)
        os.replace(temp_filename, self.filename)