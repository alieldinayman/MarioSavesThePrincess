from flask import jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, ALL, MATCH
import os
import time
import datetime

from grid_solver import GridSolver

# Initialize the Dash web app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash("Mario Saves The Princess", title="Mario Saves the Princess")
server = app.server  # Use the underlying Flask server instance in Dash

app.layout = html.Div(children=[
    html.H3(children="Grid Size", style={"display": "flex", "align-items": "center", "justify-content": "center"}),
    dcc.Slider(id="size-slider", marks={i: '{}'.format(i) for i in range(51)}, min=2, max=50, value=2),
    html.Br(),
    html.Div(id="grid", children=[])
])

# TODO: Turn these into client-side callbacks to reduce overhead on server
# Bind a callback to any dynamically created nodes/buttons
# app.clientside_callback(
#     """
#     function(size, data) {
#         var grid = []
#         for (i = 0; i < size; i++) {
#             var row = []
#             for (j = 0; j < size; i++) {
#                 row.push(html.Button(children="-", id={"type": "dynamic-node", "index": str(i) + "," + str(j)}, n_clicks=0))
#             }
#             grid.push(html.Div(children=row, style={"display": "flex", "align-items": "center", "justify-content": "center"}))
#         }
#         return grid
#     }
#     """,
#     Output(component_id="grid", component_property="children"),
#     [Input(component_id="size-slider", component_property="value")]
# )


node_pool = []
for i in range(50):
    row = []
    for j in range(50):
        row.append(html.Button(children="-", id={"type": "dynamic-node", "index": str(i) + "," + str(j)}, n_clicks=0))
    node_pool.append(row)

@app.callback(Output("grid", "children"),
              [Input("size-slider", "value")])
def update_grid(size):
    grid = []
    for x in range(size):
        row = []
        for y in range(size):
            row.append(node_pool[x][y])

        grid.append(html.Div(children=row, style={"display": "flex", "align-items": "center", "justify-content": "center"}))

    return grid


# Bind a callback to any dynamically created nodes/buttons
app.clientside_callback(
    """
    function(n_clicks) {
        node_states = ["-", "x", "m", "p"]
        return node_states[n_clicks % node_states.length]
    }
    """,
    Output(component_id={"type": "dynamic-node", "index": MATCH}, component_property="children"),
    [Input(component_id={"type": "dynamic-node", "index": MATCH}, component_property="n_clicks")]
)

# @app.callback(
#     Output(component_id={"type": "dynamic-node", "index": MATCH}, component_property="children"),
#     [Input(component_id={"type": "dynamic-node", "index": MATCH}, component_property="n_clicks")])
# def update_node(n_clicks):
#     return node_states[n_clicks % len(node_states)]


# Initialize the SQLite Database
basedir = os.path.abspath(os.path.dirname(__file__))
server.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "mario_db.sqlite")
server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Stops SQLAlchemy from adding significant overhead to the db
db = SQLAlchemy(server)
ma = Marshmallow(server)  # For serializing and deserializing SQLAlchemy models to and from JSON dicts


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
@server.route("/", methods=["GET"])
def get_index():
    # TODO: Design the main page
    return jsonify({"msg": "Welcome to the Mario Saves the Princess REST API!"})


@server.route("/gamelog", methods=["GET"])
def get_full_gamelog():
    return gamelogs_schema.jsonify(GameLog.query.all())


@server.route("/gamelog/<id>", methods=["GET"])
def get_gamelog(id):
    return gamelog_schema.jsonify(GameLog.query.get(id))


@server.route("/gamelog", methods=["DELETE"])
def clear_gamelog():
    GameLog.query.delete()
    db.session.commit()
    return jsonify({"msg": "Cleared the entire Game Log."})


@server.route("/gamelog/<id>", methods=["DELETE"])
def remove_gamelog_record(id):
    record = GameLog.query.get(id)
    db.session.delete(record)
    db.session.commit()
    return gamelog_schema.jsonify(record)


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


# Run Dash web app (with Flask server)
if __name__ == "__main__":
    print("Connecting to DB at: " + server.config["SQLALCHEMY_DATABASE_URI"])
    app.run_server(debug=True)
