from flask import request, jsonify

from Config import app

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/general_test", methods=["GET", "POST"])
def general_test():
    non_lands = request.json.get("nonLands")
    return jsonify({"message": f"We got your message: ${non_lands}"})


