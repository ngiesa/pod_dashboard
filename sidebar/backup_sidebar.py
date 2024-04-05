sidebar = html.Div(
    [
        html.H3(
                    children="POD Cockpit", className="header-title"
                ),
        html.Hr(),
        html.Div(
            children=[
                html.P(
            "14-12-2024 14:76", className="lead",  style={'display': 'inline'}
        ),
        html.I(className="fas fa-sync", style={'display': 'inline', 'padding': '10px'}),
                ], style={'padding': '0px 0px 10px 0px'}
            ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Page 1", href="/page-1", active="exact"),
                dbc.NavLink("Page 2", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar",
)