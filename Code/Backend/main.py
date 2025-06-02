from flask import request, jsonify, session, redirect
from Config import app, db

from PlayerInput import PlayerInput
from Formats import Format


@app.route("/test_input", methods=["POST"])
def test_input():
    #non_lands = request.json.get("nonLands")

    return jsonify({"message": f"\"{session.get("non_lands")}\""})

@app.route("/fetch_formats", methods=["GET"])
def fetch_formats():
    formats = Format.query.all()
    json_formats = list(map(lambda x: x.to_json(), formats))
    return jsonify({"formats": json_formats})

@app.route("/fetch_cycles", methods=["GET"])


@app.route("/set_session", methods=["POST"])
def set_session():
    non_lands = session["non_lands"] = request.json.get("nonLands")
    format = session["format"] = request.json.get("format")
    quantity = session["quantity"] = request.json.get("quantity")
    player_input = PlayerInput(non_lands, format, quantity)


    return jsonify({"message": "I think it worked?"})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)