import json
from AppFactory import create_app
from database_management.models.Cycle import Cycle
from database_management.models.Format import Format
from flask import jsonify, session, request
from flask_caching import Cache
from Extensions import db
from simulation_objects.CardCollections.Deck import Deck
from simulation_objects.CardCollections.MonteCarlo import MonteCarlo

with open("Ratadrabik.json", "r") as file:
    data = json.load(file)

app = create_app()
cache = Cache(app)

with app.app_context():
    land_options = [data["Lands"], data["AllBasics"], data["AllTowers"]]
    for option in land_options:
        print("Running (order normal, all basics, all command towers")
        deck = Deck()
        deck.setup(data["Nonlands"], data["Format"], data["Quantity"])
        monty = MonteCarlo(deck)
        monty.fill_heap(from_testlist=option)

        monty.run()





