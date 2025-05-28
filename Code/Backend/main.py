from flask import request, jsonify
from Config import app

from Session import Session

@app.route("/test_input", methods=["POST"])
def test_input():
    non_lands = request.json.get("nonLands")
    print(non_lands)
    session = Session(request.json)

    return jsonify({"message": f"\"{session.non_lands}\""})

if __name__ == "__main__":
    app.run(debug=True)