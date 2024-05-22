from dash.dependencies import Input, Output, State
from sidebar.home import render_home
from sidebar.statistics import render_statistics
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from sidebar.view_builder import build_filtered_master_table, build_details_main_view
import dash_daq
from sidebar.filter_menu import construct_filter_menu
from sidebar.statistics import build_stats

def get_callbacks(app, ddm):
    """ calls all functions with app dependency """
    
    @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
    def render_page_content(pathname):
        #TODO construct filtering here and then hand over to subpages!!! SUPER DUPEr
        filter_menu = construct_filter_menu(ddm=ddm)
        if pathname == "/":
            return render_home(ddm=ddm, filter_menu=filter_menu)
        elif pathname == "/page-1":
            return render_statistics(ddm=ddm, filter_menu=filter_menu) #TODO INCLUDE ALL THE DESIGN COMPONENTS IN ONE VIEW AND JUST HIDE AN UNHIDE WITH THE SIDE TOGGLE BAR DUE TO CALLBAKC ISSUES
        elif pathname == "/page-2":
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
    Output('master_table_content', 'children'),
    Input('age-range-slider', 'value'))
    def update_output(value):
        filter_dict = {"start_date": {"variable": "prem_age", "value": value[0], "condition": "greater"}}
        table = build_filtered_master_table(ddm=ddm, filter_condition=filter_dict)
        filter_dict = {"end_date": {"variable": "prem_age", "value": value[1], "condition": "less"}}
        table = build_filtered_master_table(ddm=ddm, filter_condition=filter_dict)
        statistics = build_stats(ddm=ddm)
        return table
        
    @app.callback(
    Output('master_table_content', 'children', allow_duplicate=True),
    Output('statistic_tiles', 'children', allow_duplicate=True),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'), prevent_initial_call=True)
    def update_output(start_date, end_date):
        filter_dict = {"start_date": {"variable": "BEGAN", "value": start_date, "condition": "greater"}}
        table = build_filtered_master_table(ddm=ddm, filter_condition=filter_dict)
        filter_dict = {"end_date": {"variable": "BEGAN", "value": end_date, "condition": "less"}}
        table = build_filtered_master_table(ddm=ddm, filter_condition=filter_dict)
        statistics = build_stats(ddm=ddm)
        return table, statistics
    
    @app.callback(
    Output('master_table_content', 'children', allow_duplicate=True),
    Output('statistic_tiles', 'children', allow_duplicate=True),
    Input('dropdown_clinical_unit', 'value'), prevent_initial_call=True)
    def update_output(value):
        print('You have selected as unit "{}"'.format(value))
        filter_dict = {"item_unit": {"variable": "prem_org_unit", "value": value, "condition": "equal"}}
        table = build_filtered_master_table(ddm=ddm, filter_condition=filter_dict)
        statistics = build_stats(ddm=ddm)
        return table, statistics
        
    @app.callback(
    Output('master_table_content', 'children', allow_duplicate=True),
    Output('statistic_tiles', 'children', allow_duplicate=True),
    Input('dropdown_surgical_area', 'value'), prevent_initial_call=True)
    def update_output(value):
        print('You have selected "{}"'.format(value))
        filter_dict = {"item_area": {"variable": "prem_area", "value": value, "condition": "equal"}}
        table = build_filtered_master_table(ddm=ddm, filter_condition=filter_dict)
        statistics = build_stats(ddm=ddm)
        return table, statistics
        
    @app.callback(
    Output('tbl_out', 'children', allow_duplicate=True), 
    Input('master_table_check', 'derived_virtual_selected_rows'), prevent_initial_call=True)
    def update_graphs(row):
        print("CLICK ")
        if row == None:
            return html.Div()
        if len(row) > 0:
            print(row[0])
            f =  build_details_main_view(ddm=ddm, index=row[0])
            return f
        
    