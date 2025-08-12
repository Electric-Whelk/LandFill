import json
import time

from AppFactory import create_app
from database_management.models.Cycle import Cycle
from database_management.models.Format import Format
from flask import jsonify, session, request
from flask_caching import Cache
from simulation_objects.CardCollections.Deck import Deck
from simulation_objects.CardCollections.MCUsrTest import MCUsrTest
from simulation_objects.CardCollections.MonteCarlo import MonteCarlo
from simulation_objects import InputParser
from flask import Flask, send_from_directory
import os
import requests

from simulation_objects.GameCards import Land

print("You're here!")

app = create_app()
cache = Cache(app)

Deck = Deck()
MonteCarlo = MonteCarlo(Deck, verbose=True)
InputParser = InputParser()
PrevPageOneInput = "DEADVALUE"
PrevPageTwoInput = "DEADVALUE"

"""status = "Dev"
match(status):
    case "UserTest":
        print("Set monty as usertest...")
        monty = MCUsrTest(deck)
    case "Dev":
        monty = MonteCarlo(deck)"""


@app.route("/card-images/<path:filename>")
def serve_card_image(filename):
    """Serve cached card images."""
    return send_from_directory(MonteCarlo.image_dir, filename)


@app.route('/api/submit-deck', methods=['POST'])
def submit_deck():
    data = request.get_json()
    with open("SubmissionLog.json", "w") as f:
        print("Writing submission to file!")
        f.write(json.dumps(data))
    print("Received data:", data)
    global PrevPageOneInput
    if data != PrevPageOneInput:
        decklist = InputParser.parse_decklist(data.get("deckList"))
        partner = InputParser.parse_partner(data.get("partner"))
        Deck.setup(decklist, data.get("commander"), partner=partner)
        MonteCarlo.setup()
        MonteCarlo.fill_heap()
        PrevPageOneInput= data
    heap = MonteCarlo.export_cycles()


    #actual response
    return jsonify({"currency": data.get("currency"), "heap": heap})

@app.route('/api/test-preferences', methods=['POST'])
def test_preferences():
    data = request.get_json()
    print("Received data:", data)
    global PrevPageTwoInput
    if data != PrevPageTwoInput:
        MonteCarlo.set_permissions(mandatory = data.get("mandatory"),
                                   permitted = data.get("permitted"),
                                   excluded = data.get("excluded"))
        MonteCarlo.set_rankings(data.get("rankings")) #NOTE THAT THESE WERE SWAPPED
        PrevPageTwoInput= data

    heap = MonteCarlo.export_cards()


    return jsonify({"cards": heap})


@app.route('/api/submit-preferences', methods=['POST'])
def submit_preferences():
    data = request.get_json()
    with open("PreferencesLog.json", "w") as f:
        print("Writing preferences to file!")
        f.write(json.dumps(data))
    print("Received data:", data)
    global PrevPageTwoInput
    if data != PrevPageTwoInput:


        MonteCarlo.set_permissions(mandatory = data.get("mandatory"),
                                   permitted = data.get("permitted"),
                                   excluded = data.get("excluded"))
        MonteCarlo.set_rankings(data.get("rankings"))

        PrevPageTwoInput= data

    MonteCarlo.run(of_each_basic = data.get("minIndividualBasics"), min_basics = data.get("minBasics"))
    #lands = [x.to_dict() for x in Deck.card_list if isinstance(x, Land) and x.permitted]
    lands = []
    nonLands = []
    for card in Deck.card_list:
        if isinstance(card, Land):
            lands.append(card.to_dict())
        else:
            nonLands.append(card.to_dict())
    output = {"lands": lands, "nonLands": nonLands, "proportions": Deck.finalscore}
    for key in output:
        print(output[key])

    return jsonify(output)






"""return jsonify({
        "message": "Received deck",
        "deckListLength": len(data.get("deckList", "").splitlines()),
        "commander": data.get("commander", ""),
        "placeholderCards": [
            {"displayName": "Shock Land", "description": "Good fixing", "image": "ShockLand.jpg"},
            {"displayName": "Fetch Land", "description": "Fetches basics", "image": "FetchLand.jpg"}
        ]
    })
        """

"""@app.route('/fetch_cycles', methods=['GET'])
def fetch_cycles():
    cycles = Cycle.query.filter(Cycle._official == True).all()
    json_cycles = list(map(lambda x: x.to_JSON(), cycles))
    return jsonify({'cycles': json_cycles})


@app.route('/fetch_formats', methods=["GET"])
def fetch_formats():
    formats = Format.query.all()
    json_formats = list(map(lambda x: x.to_JSON(), formats))
    return jsonify({'formats': json_formats})


@app.route('/lock', methods=["POST"])
def lock():
    #try:
    input_cards = session["input_cards"] = request.json.get("inputCards")
    format = session["format"] = request.json.get("format")
    quantity = session["quantity"] = request.json.get("requestedQuantity")

    deck.setup(input_cards, format, quantity)
    monty.fill_heap_CONDEMNED()

    return jsonify({"response": "Success - hey Leah shouldn't you be doing this with headers?"})
    #except Exception as e:
        #raise(e)
        #return jsonify({"response": "Failed - hey Leah shouldn't you be doing this with headers?"})

@app.route('/run', methods=["POST"])
def run():

    budget = request.json.get("budget")
    max_price_per_card = request.json.get("maxPricePerCard")
    currency = request.json.get("currency")
    threshold = request.json.get("painThreshold")
    min_basics = request.json.get("minBasics")


    monty.set_requirements(budget=budget,
                           mppc=max_price_per_card,
                           currency=currency,
                           threshold=threshold,
                           minbasics=min_basics)

    output = monty.run()
    print(output["cards"])




    return jsonify({"response": output})
    #except Exception as e:
        #print(e)
        #return jsonify({"response": "Failed - hey Leah shouldn't you be doing this with headers?"})
"""




if __name__ == '__main__':
    app.run(debug=True)

