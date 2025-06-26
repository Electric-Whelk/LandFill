from AppFactory import create_app
from database_management.models.Cycle import Cycle
from database_management.models.Format import Format
from flask import jsonify, session, request
from flask_caching import Cache
from simulation_objects.Deck import Deck
from simulation_objects.MonteCarlo import MonteCarlo

app = create_app()
cache = Cache(app)

deck = Deck()
monty = MonteCarlo(deck)


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
    try:
        input_cards = session["input_cards"] = request.json.get("inputCards")
        format = session["format"] = request.json.get("format")
        quantity = session["quantity"] = request.json.get("requestedQuantity")

        deck.setup(input_cards, format, quantity, 7)

        return jsonify({"response": "Success - hey Leah shouldn't you be doing this with headers?"})
    except Exception:
        return jsonify({"response": "Failed - hey Leah shouldn't you be doing this with headers?"})

@app.route('/run', methods=["POST"])
def run():
    try:
        budget = request.json.get("budget")
        max_price_per_card = request.json.get("maxPricePerCard")
        currency = request.json.get("currency")
        threshold = request.json.get("threshold")
        min_basics = request.json.get("minBasics")

        monty.deck.test_int = 3
        monty.test_reference = 5

        print("Test int: " + str(deck.test_int))
        return jsonify({"response": "Success - hey Leah shouldn't you be doing this with headers?"})
    except Exception as e:
        print(e)
        return jsonify({"response": "Failed - hey Leah shouldn't you be doing this with headers?"})





if __name__ == '__main__':
    app.run(debug=True)

