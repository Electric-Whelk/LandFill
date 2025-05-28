from config import db

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def to_json(self):
        #converts all the fields on the object into a python dictionary which we can convert into Json. 
        #the API will accept and create json objects to send to the frontend
        return{
            "id": self.id,
            "firstName": self.first_name, #note camelcase and snakecase (snakecase is standard for python)
            "lastName": self.last_name,
            "email": self.email, #DEBUG? am I supposed to put a comma on the last one?
        }
