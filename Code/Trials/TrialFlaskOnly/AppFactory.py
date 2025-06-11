from Extensions import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import secrets

def create_app():
    app = Flask(__name__)
    app.secret_key = secrets.token_urlsafe(32)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testmtg.db'
    db.init_app(app)
    from database.tables.Card import Card
    from database.tables.Face import Face

    with app.app_context():
        db.create_all()

    return app