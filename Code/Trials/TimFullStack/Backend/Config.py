from flask import Flask, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import sqlalchemy as db

#flask setup
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flask_mtg.db"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:../../TrialDatabase/mtg.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

flask_db = SQLAlchemy(app)
Session(app)
CORS(app, supports_credentials=True)

