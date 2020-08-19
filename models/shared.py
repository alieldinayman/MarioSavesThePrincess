from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

db = SQLAlchemy()  # ORM
ma = Marshmallow()  # For serializing and deserializing SQLAlchemy models to and from JSON dicts


# Initialize the SQLite Database
def initialize_db(server):
    # Locate the DB file
    basedir = os.path.abspath(os.path.dirname(__file__))
    server.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "../mario_db.sqlite")
    server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Stops SQLAlchemy from adding significant overhead to db

    # Feed the Flask server instance to SQLAlchemy and Marshmallow
    db.init_app(server)
    ma.init_app(server)