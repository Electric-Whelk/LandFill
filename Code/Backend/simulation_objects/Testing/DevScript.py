import json
from AppFactory import create_app
from database_management.models.Cycle import Cycle
from database_management.models.Format import Format
from flask import jsonify, session, request
from flask_caching import Cache
from Extensions import db
from simulation_objects.CardCollections.Deck import Deck
from simulation_objects.CardCollections.MonteCarlo import MonteCarlo

with open("XavierSal.json", "r") as file:
    data = json.load(file)

app = create_app()
cache = Cache(app)

close_examine = False
timer = False

with app.app_context():
    if close_examine:
        land_options = [data['AllLands']]
    else:
        #land_options = [data["AllBasics"], data["Lands"], data["AllTowers"]]
        land_options = [data["AllBasics"]]
    for option in land_options:
        print("Running allbasics, normal, all command towers")
        deck = Deck()
        deck.setup(data["Nonlands"], data["Format"], data["Quantity"])
        monty = MonteCarlo(deck, close_examine=close_examine, timer=timer)
        monty.fill_heap(from_testlist=option)
        for _ in range(1):

            monty.run()
        break





