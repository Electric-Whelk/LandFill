from Extensions import db
#from Extensions import migrate
from flask import Flask
from flask_cors import CORS
#from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import secrets

def create_app():
    app = Flask(__name__)
    CORS(app=app, supports_credentials=True)
    app.secret_key = secrets.token_urlsafe(32)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mtg.db'
    app.config['CACHE_TYPE'] = "SimpleCache"
    #app.config['CACHE_DEFAULT_TIMEOUT'] = 300
    #app.config['SQLALCHEMY_ECHO'] = True
    db.init_app(app)
#    migrate.init_app(app, db)

    from sqlalchemy import event
    from sqlalchemy.engine import Engine
    import sqlite3

    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        if isinstance(dbapi_connection, sqlite3.Connection):  # only for SQLite
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()


    from database_management.models.Card import Card
    from database_management.models.Face import Face
    from database_management.models.Cycle import Cycle
    from database_management.models.Format import Format
    from database_management.models.Intermediates import (Banned, Restricted, Legal,
    GameCards, GameFormats)


    with app.app_context():
        db.create_all()

    return app