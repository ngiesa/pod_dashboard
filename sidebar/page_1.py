from dash import dcc
from dash import html
from datetime import date
from conn.hdl.data_manager import DashDataManager
import dash_bootstrap_components as dbc

from dash import Dash, dcc, html, Input, Output, callback, dash_table
import pandas as pd
from sidebar.view_builder import build_filtered_master_table

def render_page_1(ddm: DashDataManager):
    return html.Div( 
         children=[
            html.Div(
                children= 
                html.Div(
                    children=[
                        html.H1(
                            children="Postoperative Delirium Cockpit", className="header-title"
                        ),
                        html.P(
                            children=(
                                "Interactive Implementation of Deep Learning and Baseline Information"
                            ),
                            className="header-description",
                        ),
                    ],
                    className="header"
                ),
                className="background"       
            ),
            
            
            html.Div(
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
                                            min_date_allowed=ddm.get_date_items()[0],
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
                                        
                        )
  
                    ],
        
            ),
            
            html.Div(id='tbl_out', children=[html.H1("LOADING")], style={"padding-left":"55px", 
                                                                             "padding-right":"55px",
                                                                             "padding-top":"20px",
                                                                             "padding-bottom":"20px"}),

            html.Div(
                className="master-op-table",
                children=[
                          html.Div(
                              className="master-table-container",
                              children=[
                                html.Div('Surgery Master Table (check to see details)', className = "menu-title-master"),
                                html.Div(
                                    id="master_table_content",
                                    className = "master-table-content",
                                    children=[build_filtered_master_table(ddm=ddm, filter_condition={})],
                                    ),
                            ],),
                          html.Div(id='datatable-row-ids-container'),
                ]
            )
            
        ], style={
    'background-image':'url("./assets/bed.jpg")'})
