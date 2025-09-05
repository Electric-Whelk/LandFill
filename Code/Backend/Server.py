import json
import time

from AppFactory import create_app
from database_management.models.Cycle import Cycle
from database_management.models.Format import Format
from flask import jsonify, session, request
from flask_caching import Cache
from simulation_objects.CardCollections.Deck import Deck
from simulation_objects.CardCollections.MCUsrTest import MCUsrTest
from simulation_objects.CardCollections.DeckBuilder import DeckBuilder
from simulation_objects import InputParser
from flask import Flask, send_from_directory
import os
import requests

from simulation_objects.GameCards import Land

print("You're here!")

app = create_app()
cache = Cache(app)

player_deck = Deck()
monty = DeckBuilder(player_deck, verbose=True)
imp = InputParser()
PrevPageOneInput = "DEADVALUE"
PrevPageTwoInput = "DEADVALUE"

"""status = "Dev"
match(status):
    case "UserTest":
        print("Set monty as usertest...")
        monty = MCUsrTest(deck)
    case "Dev":
        monty = monty(deck)"""


@app.route("/card-images/<path:filename>")
def serve_card_image(filename):
    """Serve cached card images."""
    return send_from_directory(monty.image_dir, filename)


@app.route('/submit-deck', methods=['POST'])
def submit_deck():
    data = request.get_json()
    #with open("RukaLandsSubs.json", "w") as f:
        #print("Writing submission to file!")
        #f.write(json.dumps(data))
    print("Received data:", data)
    #with open("output_files/deck_submissions/typical_input.json", "w") as json_file:
        #json.dump(data, json_file)
    global PrevPageOneInput
    if data != PrevPageOneInput:
        imp.refresh_deck_submission()
        player_deck.scrap_all_cards()
        monty.scrap_all_cards()


        decklist = imp.parse_decklist(data.get("deckList"))
        partner = imp.parse_partner(data.get("partner"))
        print(decklist)
        player_deck.setup(decklist, data.get("commander"), partner=partner, remove_lands = data.get("removeLands"))
        q = player_deck
        monty.setup()
        monty.fill_heap()
        PrevPageOneInput= data
    heap = monty.export_cycles()


    #actual response
    return jsonify({"currency": data.get("currency"), "heap": heap})


@app.route('/api/submit-preferences', methods=['POST'])
def submit_preferences():
    data = request.get_json()
    #with open("RukaLandsPrefs.json", "w") as f:
        #print("Writing preferences to file!")
        #f.write(json.dumps(data))
    print("Received data:", data)
    global PrevPageTwoInput
    if data != PrevPageTwoInput:
        print("RESETTING PREFERENCES")
        monty.set_permissions(mandatory = data.get("mandatory"),
                              permitted = data.get("permitted"),
                              excluded = data.get("excluded"))
        monty.set_rankings(data.get("rankings"))

        PrevPageTwoInput= data

    monty.run(of_each_basic = data.get("minIndividualBasics"), min_basics = data.get("minBasics"))
    #lands = [x.to_dict() for x in player_deck.card_list if isinstance(x, Land) and x.permitted]
    lands = []
    nonLands = []
    allCards = []
    for card in player_deck.card_list:
        if isinstance(card, Land):
            lands.append(card.to_dict())
        else:
            nonLands.append(card.to_dict())
        allCards.append(card.to_dict())


    imp.decklist_to_categories(player_deck.card_list)
    moxbox = imp.format_for_moxbox()
    archidekt = imp.format_for_archidekt()
    tappedout = imp.format_for_tappedout()
    moxboxLands = imp.format_moxbox_lands()
    archidektLands = imp.format_archidekt_lands()
    tappedoutLands = imp.format_tappedout_lands()
    output = {"lands": lands,
              "nonLands": nonLands,
              "moxbox": moxbox,
              "archidekt": archidekt,
              "tappedout": tappedout,
              "moxboxLands": moxboxLands,
              "archidektLands": archidektLands,
              "tappedoutLands": tappedoutLands,
              "proportions": player_deck.finalscore}

    monty.reset_lands()

    return jsonify(output)


"""@app.route('/api/test-preferences', methods=['POST'])
def test_preferences():
    data = request.get_json()
    print("Received data:", data)
    global PrevPageTwoInput
    if data != PrevPageTwoInput:
        monty.set_permissions(mandatory = data.get("mandatory"),
                              permitted = data.get("permitted"),
                              excluded = data.get("excluded"))
        monty.set_rankings(data.get("rankings")) #NOTE THAT THESE WERE SWAPPED
        PrevPageTwoInput= data

    heap = monty.export_cards()


    return jsonify({"cards": heap})"""





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

@app.route('/fetch_cycles', methods=['GET'])
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

    player_deck.setup(input_cards, format, quantity)
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


#PROGRESS UPDATE REFACTOR
import threading, uuid

tasks = {}  # global store: {task_id: {"status": "running", "result": None}}

import threading, uuid

tasks = {}

@app.route('/submit-preferencesV2', methods=['POST'])
def submit_preferences_V2():
    data = request.get_json()
    task_id = str(uuid.uuid4())

    # Create empty task entry
    tasks[task_id] = {
        "status": "running",
        "logs": [],
        "result": None,
    }

    # Background worker
    def run_job(task_id, data):
        with app.app_context():
            print(f"EXCLUDED: {[x["name"] for x in data.get("excluded")]}")
            print("Running")
            monty.set_permissions(mandatory=data.get("mandatory"),
                                  permitted=data.get("permitted"),
                                  excluded=data.get("excluded"))
            monty.set_rankings(data.get("rankings"))
            try:
                for update in monty.run_stream(
                    of_each_basic=data.get("minIndividualBasics"),
                    min_basics=data.get("minBasics")
                ):
                    tasks[task_id]["logs"].append(update)

                # Final output
                tasks[task_id]["result"] = build_output(player_deck, imp)
                tasks[task_id]["status"] = "done"
            except Exception as e:
                tasks[task_id]["logs"].append(f"Error: {e}")
                tasks[task_id]["status"] = "error"

    # Spawn worker thread
    thread = threading.Thread(target=run_job, args=(task_id, data))
    thread.start()

    # ✅ Return immediately
    print(f"Concluded with deck length {len(player_deck.card_list)}")
    response = jsonify({"task_id": task_id})
    print(response)
    return response


@app.route("/status/<task_id>")
def task_status(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "Invalid task_id"}), 404

    return jsonify({
        "status": task["status"],
        "logs": task.get("logs", []),   # return progress messages
    })

@app.route("/result/<task_id>")
def task_result(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "Invalid task id"}), 404
    if task["status"] != "done":
        return jsonify({"error": "Task not complete"}), 400
    return jsonify(task["result"])

def build_output(player_deck, imp):
    lands, nonLands, allCards = [], [], []
    for card in player_deck.card_list:
        if isinstance(card, Land):
            lands.append(card.to_dict())
        else:
            nonLands.append(card.to_dict())
        allCards.append(card.to_dict())

    imp.decklist_to_categories(player_deck.card_list)
    return {
        "lands": lands,
        "nonLands": nonLands,
        "moxbox": imp.format_for_moxbox(),
        "archidekt": imp.format_for_archidekt(),
        "tappedout": imp.format_for_tappedout(),
        "moxboxLands": imp.format_moxbox_lands(),
        "archidektLands": imp.format_archidekt_lands(),
        "tappedoutLands": imp.format_tappedout_lands(),
        "proportions": player_deck.finalscore
    }



if __name__ == '__main__':
    app.run(debug=True)

