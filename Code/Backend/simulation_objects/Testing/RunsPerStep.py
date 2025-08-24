import json
from AppFactory import create_app
from simulation_objects.Misc.InputParser import InputParser
from simulation_objects.CardCollections.Deck import Deck
from simulation_objects.CardCollections.MonteCarlo import MonteCarlo

from itertools import combinations
from collections import Counter


def multiset_jaccard(deck_a, deck_b):
    """
    Compute multiset Jaccard similarity between two decks.
    Each deck is a list of card names (duplicates allowed for multiple copies).
    """
    # Count how many copies of each land are in each deck
    counts_a = Counter(deck_a)
    counts_b = Counter(deck_b)

    # Find the union of all land names in both decks
    all_lands = set(counts_a.keys()) | set(counts_b.keys())

    # For each land, get min and max counts across the two decks
    min_sum = 0
    max_sum = 0
    for land in all_lands:
        count_a = counts_a.get(land, 0)  # 0 if not present
        count_b = counts_b.get(land, 0)
        min_sum += min(count_a, count_b)  # shared copies
        max_sum += max(count_a, count_b)  # total possible copies
        if land not in ["Island", "Swamp", "Forest"] and count_a > 1:
            raise Exception(f"Found {count_a} copies of {land} in a deck")

    # If both decks are empty, define similarity as 1.0 (identical)
    if max_sum == 0:
        return 1.0
    return min_sum / max_sum


def average_pairwise_jaccard(decks):
    """
    Compute the average pairwise multiset Jaccard similarity across N decks.
    decks: list of decks, where each deck is a list of land names (strings).
    """
    num_decks = len(decks)
    if num_decks < 2:
        return 1.0  # trivially identical if only one deck

    similarities = []

    # combinations(range(num_decks), 2) gives all pairs of deck indices (a,b) with a<b
    for a_idx, b_idx in combinations(range(num_decks), 2):
        sim = multiset_jaccard(decks[a_idx], decks[b_idx])
        similarities.append(sim)

    # Average over all pairs
    return sum(similarities) / len(similarities)

with open("XavNonLandsSubs.json", "r") as file:
    data = json.load(file)

with open("XavNonLandsPrefs.json", "r") as file:
    prefs = json.load(file)





app = create_app()


samplesize = 10

with app.app_context():
    manabases = []
    for _ in range(samplesize):
        deck = Deck()
        theImp = InputParser()
        decklist = theImp.parse_decklist(data.get("deckList"))
        deck.setup(decklist, data.get("commander"), partner=data.get("partner"))
        monty = MonteCarlo(deck, verbose=True)
        monty.setup()
        monty.fill_heap()
        monty.set_permissions(mandatory=prefs.get("mandatory"),
                              permitted=prefs.get("permitted"),
                              excluded=prefs.get("excluded"))
        monty.set_rankings(prefs.get("rankings"))
        monty.run(min_basics=prefs["minBasics"], of_each_basic=prefs["minIndividualBasics"])
        lands = deck.lands_list()
        landnames = [n.name for n in lands]
        manabases.append(landnames)

    avg_sim = average_pairwise_jaccard(manabases)
    print(f"Average pairwise multiset Jaccard: {avg_sim:.3f}")
