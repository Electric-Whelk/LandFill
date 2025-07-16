import pickle

class LandPermutationCache:
    def __init__(self, filename="permutation_cache.pkl"):
        self.filename = filename
        try:
            with open(filename, "rb") as f:
                self.cache = pickle.load(f)
        except FileNotFoundError:
            self.cache = {}

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache[key] = value

    def save(self):
        with open(self.filename, "wb") as f:
            pickle.dump(self.cache, f)