# from conn.hdl.data_manager import DashDataManager
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html

from ..data_manager import ddm
from ..view_builder import build_filtered_master_table


def render_home_page():
    return html.Div(
        children=[
            html.Div(
                children=html.Div(
                    children=[
                        html.H1(
                            children="Postoperative Delirium Cockpit",
                            className="header-title",
                        ),
                        html.P(
                            children=(
                                "Interactive Implementation of Deep Learning and Baseline Information"
                            ),
                            className="header-description",
                        ),
                    ],
                    className="header",
                ),
                className="background",
                style={"padding-left": "30px"},
            ),
            html.Div(
                className="filter-menu",
                children=[
                    html.Div(
                        className="filter-dropdown",
                        children=[
                            html.Div(
                                children="Clinical Unit",
                                className="menu-title",
                                style={"padding": "5px"},
                            ),
                            dcc.Dropdown(
                                id="dropdown_clinical_unit",
                                options=ddm.get_dropdown_items(
                                    pream_col="prem_org_unit"
                                ),
                                clearable=True,
                                searchable=True,
                            ),
                            html.Div(id="output_clinical_unit"),
                        ],
                        style={"padding": "10px"},
                    ),
                    html.Div(
                        className="filter-dropdown",
                        children=[
                            html.Div(
                                children="Surgical Area",
                                className="menu-title",
                                style={"padding": "5px"},
                            ),
                            dcc.Dropdown(
                                id="dropdown_surgical_area",
                                options=ddm.get_dropdown_items(pream_col="prem_area"),
                                clearable=True,
                                searchable=True,
                            ),
                            html.Div(id="output_surgical_area"),
                        ],
                        style={"padding": "10px"}
                    ),
                    html.Div(
                        className="filter-dropdown",
                        children=[
                            html.Div(
                                children="Surgery Dates",
                                className="menu-title",
                                style={"padding": "5px"},
                            ),
                            dcc.DatePickerRange(
                                id="date-picker-range",
                                min_date_allowed=ddm.get_date_items()[0],
                                max_date_allowed=ddm.get_date_items()[1],
                                start_date=ddm.get_date_items()[1]
                                - pd.Timedelta(weeks=1),
                                end_date=ddm.get_date_items()[1],
                            ),
                            html.Div(id="output-date-picker"),
                        ],
                        style={"padding": "10px"},
                    ),
                    html.Div(
                        className="pick-ranger",
                        children=[
                            html.Div(children="Age Range", className="menu-title"),
                            dcc.RangeSlider(
                                0, 100, 5, value=[0, 100], id="age-range-slider"
                            ),
                            html.Div(id="age-output"),
                        ],
                        style={"padding": "10px"}
                    ),
                ],
                style={
                    "border-radius": "10px",
                    # "padding": "10px",
                    "padding": "30px",
                    "background-color": "#f8f9fa",
                    "border": "2px solid #f8f9fa",
                    "margin-top": "50px",
                    "margin-bottom": "30px",
                    # "padding-left": "30px",
                    # "padding-right": "30px",
                },
            ),
            # TODO: PHA: When should this be shown?
            # html.Div(
            #     children=[
            #         html.Div(dbc.Spinner(color="primary"), style={"display": "inline-block"}),
            #         html.Div(html.H3("Loading"), style={"display": "inline-block"})
            #     ],
            #     id="tbl_out",
            #     # # Align in center
            #     style={
            #         "display": "flex",
            #         "justify-content": "center"
            #     }
            # ),
            html.Div(
                className="master-op-table",
                children=[
                    html.Div(
                        className="master-table-container",
                        children=[
                            html.Div(
                                "Surgery Master Table (check to see details)",
                                className="menu-title-master",
                            ),
                            html.Div(
                                id="master_table_content",
                                className="master-table-content",
                                children=[
                                    build_filtered_master_table(
                                        ddm=ddm, filter_condition={}
                                    )
                                ],
                            ),
                        ],
                    ),
                    html.Div(id="datatable-row-ids-container"),
                ],
                style={
                    "border-radius": "10px",
                    "padding": "10px",
                    "background-color": "#f8f9fa",
                    "border": "2px solid #f8f9fa",
                },
            ),
        ],
        style={"background-image": 'url("./assets/bed.jpg")'},
    )
