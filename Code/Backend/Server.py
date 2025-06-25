from AppFactory import create_app
from database_management.models.Cycle import Cycle
from database_management.models.Format import Format
from flask import jsonify, session, request
from simulation_objects.Deck import Deck

app = create_app()


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
    input_cards = session["input_cards"] = request.json.get("inputCards")
    format = session["format"] = request.json.get("format")
    quantity = session["quantity"] = request.json.get("requestedQuantity")

    deck = Deck(input_cards, format, quantity)
    print(f"Requires pips: {deck.colors_needed}")

    return jsonify({"card_list": f"Cardlist: {input_cards}"})


if __name__ == '__main__':
    app.run(debug=True)

