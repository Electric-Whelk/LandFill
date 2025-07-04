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
    deck = Deck()
    deck.setup(data["Nonlands"], data["Format"], data["Quantity"])
    monty = MonteCarlo(deck)
    monty.fill_heap(from_testlist=data["Lands"])

    monty.run()





