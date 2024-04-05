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
import sidebar.data_functions as dfun
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from sidebar.page_1 import render_page_1

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://use.fontawesome.com/releases/v5.7.2/css/all.css'], suppress_callback_exceptions=False)


# the styles for the main content position it to the right of the sidebar and
# add some padding.

#TODO CHECK OUT MODEL OUTPUTS [1:46 PM] Haufe, Stefan
# Brier scores, proper scoring rules #TODO check on these metrics calibration.... 

sidebar = html.Div(
    [
        html.H3(
                    children="POD Cockpit", className="header-title"
                ),
        html.Hr(),
        html.Div(
            children=[
                html.P(
                    dfun.ddm.get_last_updated(), className="lead",  style={'display': 'inline'}
        ),
        html.I(className="fas fa-sync", style={'display': 'inline', 'padding': '10px'}),
                ], style={'padding': '0px 0px 10px 0px'}
            ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Statistics", href="/page-1", active="exact"),
                dbc.NavLink("Metrics", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar",
)

content = html.Div(id="page-content", className="content")

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

from sidebar.callbacks import get_callbacks
get_callbacks(app=app, ddm=dfun.ddm)

#TODO DASH COMPONENT LAYOUTS https://dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/ work with width sizes!!!

if __name__ == "__main__":
    #app.run_server(port=8088)
    app.run(debug=True, port=5001)