from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize the Flask web app
app = Flask("Mario Saves The Princess")
basedir = os.path.abspath(os.path.dirname(__file__))

# Initialize the SQLite Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "mario_db.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Stops SQLAlchemy from adding significant overhead to the db
db = SQLAlchemy(app)


class GameLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grid = db.Column(db.String(10000))
    paths = db.Column(db.String(1000))
    error_flag = db.Column(db.Boolean)
    req_time = db.Column(db.DateTime)
    res_duration = db.Column(db.Float)


@app.route("/", methods=["GET"])
def index_get():
    return jsonify({"msg": "Hello API!"})


if __name__ == "__main__":
    print("Connecting to DB at: " + app.config["SQLALCHEMY_DATABASE_URI"])
    app.run(debug=True)
