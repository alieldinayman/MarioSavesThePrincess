import dash

from views.layout import layout
from views.callbacks import register_callbacks
from routes.api_endpoints import register_endpoints
from models.shared import initialize_db

# Initialize the Dash web app
app = dash.Dash(__name__, title="Mario Saves the Princess")
# Use the underlying Flask server instance in Dash
server = app.server

# Front-end: Dash layout and registering callbacks
app.layout = layout
register_callbacks(app)

# Back-end: SQLite DB initialization and Flask REST API endpoint routing
initialize_db(server)
register_endpoints(server)

# Run the Dash web app (with Flask server)
if __name__ == "__main__":
    print("Connecting to DB at: " + server.config["SQLALCHEMY_DATABASE_URI"])
    app.run_server(debug=True)
