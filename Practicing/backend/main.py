#CRUD app - create read update delete; we need operations for all of these. We can think of these as four "endpoints".
#a server, for example, has an address, ie, localhost:5000. An endpoint is anything that comes after this domain, ie,
#localhost:5000/home. In this case, if we hit an endpoint such as /create_content in our frontend, we need to provide the
#firstname, email and last name used in creation. So the request headers (I think) will be the type and the json data containing
#that information. 

from flask import request, jsonify
from config import app, db
from models import Contact

@app.route("/contacts", methods=["GET"]) #this says that if we're at the /contacts endpoint, we can only accept GET requests.
def get_contacts():
    contacts = Contact.query.all() #use SQLalchemy to  get a list of all contacts in the database
    json_contacts = list(map(lambda x: x.to_json(), contacts)) #map takes the elements and gives us the result in a new list it returns a map objectw e conver to a list
    return jsonify({"contacts": json_contacts})

@app.route("/create_contact", methods=["POST"])
def create_contact():
    first_name = request.json.get("firstName") #.get handles if the entry is not found
    last_name = request.json.get("lastName")
    email = request.json.get("email")

    if not first_name or not last_name or not email:
        return (
            jsonify({"message": "You must include a first name, last name or email"}),
            400, #note you don't ned to include the successful message in get_contacts because it's presumed
        )
    
    new_contact = Contact(first_name=first_name, last_name=last_name, email=email)
    try:
        db.session.add(new_contact)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
    return jsonify({"message": "User created!"}), 201

@app.route("/update_contact/<int:user_id>", methods=["PATCH", "POST"])
def update_contact(user_id):
    contact = contact.query.get(user_id)

    if not contact:
        return jsonify({"message": "User not found"}), 404
    
    data = request.json
    contact.first_name = data.get("firstName", contact.first_name) #modify first name to be equal to the json data here
    contact.last_name = data.get("lastName", contact.last_name)
    contact.email = data.get("email", contact.email)

    db.session.commit()

    return jsonify({"message": "User updated."}), 200

@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    contact = contact.query.get(user_id)

    if not contact:
        return jsonify({"message": "User not found"}), 404
    
    db.session.delete(contact)
    db.session.commit()

    return jsonify({"message": "User deleted"}), 200


if __name__ == "__main__": #this protects us from running this file if it is imported; it has tobe run directly
    with app.app_context():
        db.create_all() #creates the database if it doesn't exist
    app.run(debug=True)