from dash.dependencies import Input, Output, State
from flask import request
import requests


def register_callbacks(app):

    # Bind a client-side callback to the Slider to dynamically create nodes/buttons
    app.clientside_callback(
        """
        function(size, n_clicks) {
            var solution = document.getElementById("solution");
            if (solution != null) {
                solution.style.display = "none";
            }

            var grid = document.getElementById("grid");
            if(grid != null) {
                grid.remove();
            }

            var div = document.createElement("div");
            div.id = "grid";
            div.align = "center";

            for (var i = 0; i < size ; i++) {
                for(var j = 0; j < size; j++) {
                    var elem = document.createElement("input");
                    elem.type = "button"
                    elem.id = "node_" + i + "_" + j;
                    elem.value = "-";
                    elem.style.backgroundColor = "#F5FFFA";
                    elem.style.width = "25px"
                    elem.style.height = "25px"
                    elem.style.fontSize = "20px";
                    elem.onclick = function() {
                        if(this.value == "-") { this.value = "x"; this.style.backgroundColor = "#FF4500"; }
                        else if (this.value == "x") { this.value = "m"; this.style.backgroundColor = "#4169E1"; }
                        else if (this.value == "m") { this.value = "p"; this.style.backgroundColor = "#ADFF2F"; }
                        else if (this.value == "p") { this.value = "-"; this.style.backgroundColor = "#F5FFFA"; }
                    }

                    div.appendChild(elem);
                }
                var br = document.createElement('br');
                div.appendChild(br);
            }

            document.body.appendChild(div);
        }
        """,
        Output(component_id="hidden-div", component_property="children"),
        [Input(component_id="size-slider", component_property="value"),
         Input(component_id="clear-btn", component_property="n_clicks")]
    )

    # Bind a client-side callback to the Solve button that converts the button grid to a valid format for the REST API
    app.clientside_callback(
        """
        function(n_clicks, size) {        
            if(n_clicks != null) {
                var solution = document.getElementById("solution");
                if (solution != null) {
                    solution.style.display = "flex";
                }
                var nodes = document.getElementById("grid").getElementsByTagName("input");
                str = ""

                for(i = 0; i < nodes.length; i++)
                {
                    str += nodes[i].value;
                }

                return str;
            }
        }
        """,
        Output(component_id="grid-string", component_property="children"),
        [Input(component_id="solve-btn", component_property="n_clicks")],
        [State(component_id="size-slider", component_property="value")]
    )

    # Bind a server-side callback to the hidden grid-string that contains the valid format of the button grid
    # that calls the "/solve" endpoint of the REST API
    @app.callback(
        Output(component_id="solution", component_property="children"),
        [Input(component_id="grid-string", component_property="children")],
        [State(component_id="size-slider", component_property="value"),
         State(component_id="solve-btn", component_property="n_clicks")]
    )
    def solve(grid_string, size, n_clicks):
        if n_clicks is not None:
            grid = []
            row = []
            count = 0
            for i in range(size ** 2):
                count += 1
                row.append(grid_string[i])

                if count % size == 0:
                    grid.append(row)
                    row = []
                    count = 0

            ans = requests.post(url=request.host_url + "/solve", json={"n": size, "grid": grid})
            return "API Output: " + str(ans.json())
