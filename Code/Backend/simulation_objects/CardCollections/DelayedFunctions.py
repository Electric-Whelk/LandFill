import pickle

from simulation_objects.Simulations import Game
from joblib import Parallel, delayed


def run_tests_exterior(deck, turns, verbose):
    g = Game(deck, turns=turns, verbose=verbose)
    g.run()
    return g