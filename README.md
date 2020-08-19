<p align="center">
  <img src="https://github.com/alieldinayman/MarioSavesThePrincess/blob/master/assets/python-mario.png?raw=true">
</p>

Mario Saves the Princess is a Dash web app that is designed to solve any grid by finding the shortest path between a start and goal nodes (Mario and the Princess).
Try it out at: https://mariosavestheprincess.herokuapp.com/

## The Algorithm
The app uses the A* search algorithm which is an efficient pathfinding algorithm, and arguably the most optimal one. A* ensures that the result is always the shortest path and runs much faster than its counterpart Dijstkra's algorithm. Learn more about the algorithm on: https://en.wikipedia.org/wiki/A*_search_algorithm

## Built on Dash
Mario Saves the Princess was built on [Plotly's Dash](https://plotly.com/dash/), a powerful web framework built on Flask, designed specifically for building Python web apps. The way Dash is structured allows for using its underlying Flask server to access all of Flask's functionality, as well as allowing for using the numerous Python libraries that integrate seamlessly with Flask such as [SQLAlchemy ORM](https://flask-sqlalchemy.palletsprojects.com/) and [Marshmallow](https://flask-marshmallow.readthedocs.io/).

## REST API
Mario Saves the Princess utilizes this functionality to be able to serve a REST API for end users. The endpoints are as follows:
* **/solve** (POST): Solves an input grid with a specified size and returns the solution as an error_flag boolean which is True if an error occurred while validating the grid data (in case of the existence of more than one Mario or Princess or none at all, for example) or if there is no valid path from Mario to the Princess. The other output is the shortest possible set of movements to reach the Princess from Mario.
  
  The input, solution, request time, and response duration (from input to server response) are then saved in the DB as Game Logs.
  
  **Example input:**  
  `{  
       "n": 3,  
       "grid": [["m", "-", "-"], ["-", "x", "x"], ["-", "-", "p"]]  
  }  `
  
  **Output:**  
`{"error_flag": false, paths": ["DOWN","DOWN","RIGHT","RIGHT"]}`

* **/gamelog** (GET, DELETE): # Fetches/clears the entire game log data from the embedded serverless SQLite database.

* **/gamelog/id** (GET, DELETE): # Fetches/removes a specific log from the DB.

  **Example of a Game Log:**  
    `{
        "error_flag": false,
        "grid": "[['m', '-', '-'], ['-', 'x', 'x'], ['-', '-', 'p']]",
        "id": 227,
        "paths": "['DOWN', 'DOWN', 'RIGHT', 'RIGHT']",
        "req_time": "2020-08-19T15:05:51.267585",
        "res_duration": 0.0003425651229918003
    }`
