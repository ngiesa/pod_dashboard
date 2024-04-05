import dash_bootstrap_components as dbc
from dash import Input, Output, html
from loguru import logger

from ..data_manager import ddm
from ..view_builder import build_details_main_view, build_filtered_master_table
from . import about, home


def route(app):
    @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
    def render_page_content(pathname):
        if pathname == "/":
            return home.render_home_page()
        elif pathname == "/about":
            return about.render_about_page()
        elif pathname == "/statistics":
            return html.Div(
                children=[
                    html.H1(
                        children="This is a sunmmary page with prevalences over time etc.",
                        className="header-title",
                    )
                ]
            )
        elif pathname == "/metrics":
            return html.P("Oh cool, this is page 2 including performance insights!")
        # If the user tries to reach a different page, return a 404 message
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ]
        )

    @app.callback(
        Output("master_table_content", "children"), Input("age-range-slider", "value")
    )
    def update_output(value):
        filter_dict = {
            "start_date": {
                "variable": "prem_age",
                "value": value[0],
                "condition": "greater",
            }
        }
        table = build_filtered_master_table(ddm=ddm, filter_condition=filter_dict)
        filter_dict = {
            "end_date": {"variable": "prem_age", "value": value[1], "condition": "less"}
        }
        table = build_filtered_master_table(ddm=ddm, filter_condition=filter_dict)
        return table

    @app.callback(
        Output("master_table_content", "children", allow_duplicate=True),
        Input("date-picker-range", "start_date"),
        Input("date-picker-range", "end_date"),
        prevent_initial_call=True,
    )
    def update_output(start_date, end_date):
        filter_dict = {
            "start_date": {
                "variable": "BEGAN",
                "value": start_date,
                "condition": "greater",
            }
        }
        table = build_filtered_master_table(ddm=ddm, filter_condition=filter_dict)
        filter_dict = {
            "end_date": {"variable": "BEGAN", "value": end_date, "condition": "less"}
        }
        table = build_filtered_master_table(ddm=ddm, filter_condition=filter_dict)
        return table

    @app.callback(
        Output("master_table_content", "children", allow_duplicate=True),
        Input("dropdown_clinical_unit", "value"),
        prevent_initial_call=True,
    )
    def update_output(value):
        logger.info('You have selected as unit "{}"'.format(value))
        filter_dict = {
            "item_unit": {
                "variable": "prem_org_unit",
                "value": value,
                "condition": "equal",
            }
        }
        table = build_filtered_master_table(ddm=ddm, filter_condition=filter_dict)
        return table

    @app.callback(
        Output("master_table_content", "children", allow_duplicate=True),
        Input("dropdown_surgical_area", "value"),
        prevent_initial_call=True,
    )
    def update_output(value):
        logger.info('You have selected "{}"'.format(value))
        filter_dict = {
            "item_area": {"variable": "prem_area", "value": value, "condition": "equal"}
        }
        table = build_filtered_master_table(ddm=ddm, filter_condition=filter_dict)
        return table

    @app.callback(
        Output("tbl_out", "children", allow_duplicate=True),
        Input("master_table_check", "derived_virtual_selected_rows"),
        prevent_initial_call=True,
    )
    def update_graphs(row):
        logger.info("CLICK ")
        if len(row) > 0:
            logger.info(row[0])
            f = build_details_main_view(ddm=ddm, index=row[0])
            return f
        return html.Div()
