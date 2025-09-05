import json

import time
import numpy
import scipy
from scipy.stats import skew, kurtosis, mode

from AppFactory import create_app
from Server import imp
from database_management.models.Cycle import Cycle
from database_management.models.Format import Format
from flask import jsonify, session, request
from flask_caching import Cache
from simulation_objects.CardCollections.Deck import Deck
from simulation_objects.CardCollections.DeckBuilder import DeckBuilder
from simulation_objects.Simulations import MonteCarlo

with open("XavierSal.json", "r") as file:
    data = json.load(file)

app = create_app()
cache = Cache(app)

allbasics = data.get("AllBasics")
onecheck = data.get("OneCheck")
oneshock = data.get("OneShock")
nobasics = data.get("NoBasics")
asibuild = data.get("AsIBuild")
alltowers = data.get("AllTowers")
halfwaythere = data.get("HalfwayThere")

options = [onecheck, oneshock]
names = ["ShockDeck", "CheckDeck"]

outputs = {}

for name in names:
    outputs[name] = []

with app.app_context():
    start = time.time()
    n = 100
    for option, name in zip(options, names):
        deckscores = []
        for _ in range(n):
            decklist = f"{data.get("Nonlands")}\n{option}"
            deck = Deck()
            deck.setup(decklist, data["Commander"])
            trial = MonteCarlo(deck)
            trial.individual_deck_test()
            #outputs[name].append(trial.game_proportions)
            wasted = trial.wasted_mana
            deckscores.append(wasted)
        #as_json = json.dumps({"outputs": deckscores})
        with open(f'output_files/deck_assessment_multiruns/{name}.json', 'w', encoding='utf-8') as f:
            json.dump({"outputs":deckscores}, f, ensure_ascii=False, indent=4)
    print(f"Took {time.time() - start} seconds")




            #outputs[name].append(f"Mean: {numpy.mean(wasted)} Mode: {mode(wasted)} Median: {numpy.median(wasted)} Skew: {skew(wasted)} Kurtosis: {kurtosis(wasted)}")
            #outputs[name].extend(wasted)

            #outputs[name] = trial.determine_cumulative_distribution()



    #commenting out so you don't accidentally overwrite if you hit play!
    #for name in names:
        #with open(f"output_files/histogram_fodder/{name}.txt", "w") as file:
            #for output in outputs[name]:
                #file.write(f"{output}\n")


    for key in outputs:
        print(f"{key}: {outputs[key]}")


        #self, input_cards, commander_name, partner = None):
