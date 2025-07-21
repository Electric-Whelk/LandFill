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
    i = 0
    if close_examine:
        land_options = [data['AsIBuild']]
    else:
        #tomorrow see if the results are starker if you start the game with everything better than a basic
        #and how a guildgate performs
        #and an option for "cheap better-than-basics"
        #land_options = [data["UnevenBasics"], data["Bad"]]
        #land_options = [data["UnevenBasics"], data["OneDiff"], data["OneGood"], data["OneEstuary"], data["OneTower"], data["Bad"]]
        #titles = ["Basics", "Check", "Shock", "Snarl", "Command Tower", "Guildgate"]

        #land_options = [data["PropCheck"], data["PropShock"]]
        #titles = ["Check", "Shock"]

        #land_options = [data["AllBasics"], data["NoBasics"], data["AsIBuild"]]
        #titles = ["All Basics", "No Basics", "Mix"]

        #land_options = [data["AsIBuild"], data["NoFetch"]]
        #titles = ["AsIBuild", "NoFetch"]

        #land_options = [data["AsIBuild"]]
        #titles = ["As i build"]

        land_options = [data["Handcrank"]]
        titles = ["Handcrank"]

    for option in land_options:
        if not close_examine:
            print(titles[i])
        deck = Deck()
        deck.setup(data["Nonlands"], data["Format"], data["Quantity"])
        monty = MonteCarlo(deck, close_examine=close_examine, timer=timer)
        monty.fill_heap(from_testlist=option)
        #monty.dev_run()
        #break
        for _ in range(1):

            monty.run()
        i += 1
        print("")





