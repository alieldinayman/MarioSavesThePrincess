from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import time
import datetime

from grid_solver import GridSolver

# Initialize the Flask web app
app = Flask("Mario Saves The Princess")
basedir = os.path.abspath(os.path.dirname(__file__))

# Initialize the SQLite Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "mario_db.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Stops SQLAlchemy from adding significant overhead to the db
db = SQLAlchemy(app)
ma = Marshmallow(app)  # For serializing and deserializing SQLAlchemy models to and from JSON dicts


# GameLog Model
class GameLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grid = db.Column(db.String(10000))
    paths = db.Column(db.String(1000))
    error_flag = db.Column(db.Boolean)
    req_time = db.Column(db.DateTime, default=datetime.datetime.now())
    res_duration = db.Column(db.Float)

    def __repr__(self):
        return '<Log %r>' % self.req_time.strftime("%d-%m-%Y (%H:%M:%S)")


# GameLog Schema
class GameLogSchema(ma.Schema):
    class Meta:
        fields = ("id", "grid", "paths", "error_flag", "req_time", "res_duration")


# Initialize Schemas
gamelog_schema = GameLogSchema()
gamelogs_schema = GameLogSchema(many=True)


# Routes
@app.route("/", methods=["GET"])
def get_index():
    # TODO: Design the main page
    return jsonify({"msg": "Welcome to the Mario Saves the Princess REST API!"})


@app.route("/gamelog", methods=["GET"])
def get_full_gamelog():
    return gamelogs_schema.jsonify(GameLog.query.all())


@app.route("/gamelog/<id>", methods=["GET"])
def get_gamelog(id):
    return gamelog_schema.jsonify(GameLog.query.get(id))


@app.route("/gamelog", methods=["DELETE"])
def clear_gamelog():
    GameLog.query.delete()
    db.session.commit()
    return jsonify({"msg": "Cleared the entire Game Log."})


@app.route("/gamelog/<id>", methods=["DELETE"])
def remove_gamelog_record(id):
    record = GameLog.query.get(id)
    db.session.delete(record)
    db.session.commit()
    return gamelog_schema.jsonify(record)


@app.route("/solve", methods=["POST"])
def solve_grid():
    tick = time.perf_counter()
    grid_solver = GridSolver()
    paths, error_flag = grid_solver.solve_grid(request.json["n"], request.json["grid"])
    tock = time.perf_counter()

    new_log = GameLog(grid=str(request.json["grid"]), paths=str(paths), error_flag=error_flag, res_duration=tock-tick)
    db.session.add(new_log)
    db.session.commit()

    return jsonify({"paths": paths, "error_flag": error_flag})


# Run Flask server
if __name__ == "__main__":
    print("Connecting to DB at: " + app.config["SQLALCHEMY_DATABASE_URI"])
    app.run(debug=True)
