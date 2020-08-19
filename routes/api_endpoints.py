from flask import jsonify, request
from models.shared import db
from models.gamelog import GameLog, gamelog_schema, gamelogs_schema
from controllers.grid_solver import GridSolver
import time


# Register the API endpoints to the Flask server's REST API
def register_endpoints(server):

    # API welcome message (placeholder endpoint)
    @server.route("/", methods=["GET"])
    def get_index():
        return jsonify({"msg": "Welcome to the Mario Saves the Princess REST API!"})

    # Fetch the entire Game log data from the DB
    @server.route("/gamelog", methods=["GET"])
    def get_full_gamelog():
        return gamelogs_schema.jsonify(GameLog.query.all())

    # Fetch a specific log by ID from the DB
    @server.route("/gamelog/<id>", methods=["GET"])
    def get_gamelog(id):
        return gamelog_schema.jsonify(GameLog.query.get(id))

    # Clear the entire Game log from the DB
    @server.route("/gamelog", methods=["DELETE"])
    def clear_gamelog():
        GameLog.query.delete()
        db.session.commit()
        return jsonify({"msg": "Cleared the entire Game Log."})

    # Delete a specific log by ID from the DB
    @server.route("/gamelog/<id>", methods=["DELETE"])
    def remove_gamelog_record(id):
        record = GameLog.query.get(id)
        db.session.delete(record)
        db.session.commit()
        return gamelog_schema.jsonify(record)

    # Solve an input grid with a specified size and returns the solution as an error_flag and paths to the goal
    # The input, solution, request time, and response duration (from input to server response) are then saved in the DB
    # Inputs to the endpoint: n -> Desired grid size, grid -> grid data as an array of grid rows (example below)
    # Input:
    # {
    #   "n": 3,
    #   "grid": [["m", "-", "-"],
    #            ["-", "x", "x"],
    #            ["-", "-", "p"]]
    # }
    # Output:
    # {
    #   "error_flag": false,
    #   "paths": ["DOWN","DOWN","RIGHT","RIGHT"]
    # }
    @server.route("/solve", methods=["POST"])
    def solve_grid():
        tick = time.perf_counter()
        grid_solver = GridSolver()
        paths, error_flag = grid_solver.solve_grid(request.json["n"], request.json["grid"])
        tock = time.perf_counter()

        new_log = GameLog(grid=str(request.json["grid"]), paths=str(paths), error_flag=error_flag, res_duration=tock-tick)
        db.session.add(new_log)
        db.session.commit()

        return jsonify({"paths": paths, "error_flag": error_flag})