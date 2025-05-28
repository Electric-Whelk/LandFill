from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__) #initializes flask application
CORS(app) #wrap our app in CORS, disabling a common error and allowing cross origin requests

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db" #specifying location of the database we're storing on our machine
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False #not tracking modifications we make to the database

db = SQLAlchemy(app) #creates a database instance giving access to stuff. Creates an ORM, object relational mapping. 

