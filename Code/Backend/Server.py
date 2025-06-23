from AppFactory import create_app
from database_management.models.Format import Format
from flask import jsonify, session, request

app = create_app()


@app.route('/fetch_formats', methods=["GET"])
def fetch_formats():
    formats = Format.query.all()
    json_formats = list(map(lambda f: f.to_JSON(), formats))
    return jsonify({'formats': json_formats})

@app.route('/lock', methods=["POST"])
def lock():
    input_cards = session["non_lands"] = request.json.get("inputCards")
    format = session["format"] = request.json.get("format")
    quantity = session["quantity"] = request.json.get("requestedQuantity")


    return jsonify({"card_list": f"Cardlist: {input_cards}"})


if __name__ == '__main__':
    app.run(debug=True)

