import dash_core_components as dcc
import dash_html_components as html

layout = html.Div(children=[
    html.Div([html.Img(src="/assets/python-mario.png"), html.H2("Mario Saves the Princess - An A* Pathfinder")],
             className="banner", style={"display": "flex", "align-items": "center", "justify-content": "center"}),
    html.H3(children="Grid Size", style={"display": "flex", "align-items": "center", "justify-content": "center"}),
    dcc.Slider(id="size-slider", marks={i: '{}'.format(i) for i in range(51)}, min=2, max=50, value=2),
    html.Div(id="hidden-div", style={"display": "none"}),
    html.Br(),
    html.Div([html.Button("Solve", id="solve-btn", className="button-primary", style={"background-color": "rgb(154,205,50"}),
             html.Button("Clear", id="clear-btn", className="button-primary", style={"background-color": "rgb(250, 128, 114)"})],
             style={"display": "flex", "align-items": "center", "justify-content": "center"}),
    html.Br(),
    html.H4(id="solution", style={"display": "flex", "align-items": "center", "justify-content": "center"}),
    html.H6(id="grid-string", style={"display": "none"}),
    html.Br(),
    html.Div([html.H6("- = Empty,", style={"display": "inline", "margin-right": "5px", "color": "rgb(169,169,169)"}),
    html.H6("X = Obstacle,\t", style={"display": "inline", "margin-right": "5px", "color": "rgb(255,69,0)"}),
    html.H6("M = Mario/Start,\t", style={"display": "inline", "margin-right": "5px", "color": "rgb(65,105,225)"}),
    html.H6("P = Princess/Goal\t", style={"display": "inline", "margin-right": "5px", "color": "rgb(154,205,50"})],
             style={"display": "flex", "align-items": "center", "justify-content": "center"})

])