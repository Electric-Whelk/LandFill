from flask import request, jsonify, session, redirect
from Config import app, flask_db

from PlayerInput import PlayerInput
from FlaskFormats import FlaskFormat

import sys
sys.path.insert(1, '../../TrialDatabase/')
from Format import Format
from Configure_DB import engine
from Configure_DB import session as dbsesh


@app.route("/test_input", methods=["POST"])
def test_input():
    #non_lands = request.json.get("nonLands")

    return jsonify({"message": f"\"{session.get("non_lands")}\""})

@app.route("/fetch_formats_flask", methods=["GET"])
def fetch_formats_flask():
    formats = FlaskFormat.query.all()
    json_formats = list(map(lambda x: x.to_json(), formats))
    print(json_formats)
    return jsonify({"formats": json_formats})

@app.route("/fetch_formats_pure_sql", methods=["GET"])
def fetch_formats_pure_sql():
    formats = dbsesh.query(Format).all()
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
        flask_db.create_all()
    app.run(debug=True)