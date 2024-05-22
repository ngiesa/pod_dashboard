
from conn.hdl.data_manager import DashDataManager
from dash import  html, dcc
import pandas as pd
import dash_daq

def construct_filter_menu(ddm: DashDataManager):
        if ddm.filter_menu is not None:
                print("return filter menu")
                return ddm.filter_menu 
        print("construct new filter menu")
        filter_menu = html.Div(
                        className="filter-menu", children=[
                                html.Div(className='filter-dropdown', 
                                        children=[
                                                html.Div(children="Clinical Unit", className="menu-title"),
                                                dcc.Dropdown(
                                                        id='dropdown_clinical_unit',
                                                        options=ddm.get_dropdown_items(pream_col="prem_org_unit"),
                                                        clearable=True,
                                                        searchable=True,
                                                        ), 
                                                html.Div(id='output_clinical_unit')],
                                        )
                                , html.Div(className='filter-dropdown', 
                                        children=[
                                                html.Div(children="Surgical Area", className="menu-title"),
                                                dcc.Dropdown(
                                                        id='dropdown_surgical_area',
                                                        options=ddm.get_dropdown_items(pream_col="prem_area"),
                                                        clearable=True,
                                                        searchable=True,
                                                        ), 
                                                html.Div(id='output_surgical_area')
                                                ]
                                        ),
                                
                                html.Div(className='filter-dropdown',
                                        children=[
                                        html.Div(
                                                children="Surgery Dates", className="menu-title"
                                                ),
                                        dcc.DatePickerRange(
                                                id='date-picker-range',
                                                min_date_allowed= pd.to_datetime("2024-01-01 00:00"),
                                                max_date_allowed=ddm.get_date_items()[1],
                                                start_date=ddm.get_date_items()[1]-pd.Timedelta(weeks=1),
                                                end_date=ddm.get_date_items()[1],
                                                ),
                                        html.Div(id='output-date-picker')], 
                                        ),
                                                        
                                html.Div(className='pick-ranger',  
                                        children=[
                                        html.Div(children="Age Range", className="menu-title"),
                                        dcc.RangeSlider(0, 100, 5, value=[0, 100], id='age-range-slider'), 
                                        html.Div(id='age-output')
                                        ],
                                        
                                                
                                ),
                        ],
                
                )
        ddm.filter_menu = filter_menu
        return filter_menu
