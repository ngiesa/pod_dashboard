"""
This app creates a simple sidebar layout using inline style arguments and the
dbc.Nav component.

dcc.Location is used to track the current location, and a callback uses the
current location to render the appropriate page content. The active prop of
each NavLink is set automatically according to the current pathname. To use
this feature you must install dash-bootstrap-components >= 0.11.0.

For more details on building multi-page Dash applications, check out the Dash
documentation: https://dash.plot.ly/urls
"""
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

from src.data_manager import ddm
# from src.callbacks import get_callbacks
from src.pages import router

app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://use.fontawesome.com/releases/v5.7.2/css/all.css",
    ],
    suppress_callback_exceptions=False,
)


# the styles for the main content position it to the right of the sidebar and
# add some padding.

# TODO CHECK OUT MODEL OUTPUTS [1:46 PM] Haufe, Stefan
# Brier scores, proper scoring rules #TODO check on these metrics calibration....

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

sidebar = html.Div(
    [
        html.H3(children="POD Cockpit", className="header-title"),
        html.Div(
            children=[
                html.P(
                    ddm.get_last_updated(),
                    className="lead",
                    style={"display": "inline"},
                ),
                html.I(
                    className="fas fa-sync",
                    style={"display": "inline", "padding": "10px"},
                ),
            ],
            style={"padding": "0px 0px 10px 0px"},
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Statistics", href="/statistics", active="exact"),
                dbc.NavLink("Metrics", href="/metrics", active="exact"),
                dbc.NavLink("About", href="/about", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar",
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", className="content")

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

app.layout = html.Div([dcc.Location(id="url"), sidebar, content], style=CONTENT_STYLE)


router.route(app=app)

# TODO DASH COMPONENT LAYOUTS https://dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/ work with width sizes!!!

if __name__ == "__main__":
    # app.run_server(port=8088)
    app.run(debug=True, port=5001)
