from dash import dcc
from dash import html
from datetime import date
from conn.hdl.data_manager import DashDataManager
import dash_bootstrap_components as dbc

from dash import Dash, dcc, html, Input, Output, callback, dash_table
import pandas as pd
from sidebar.view_builder import build_filtered_master_table
import dash_daq

def render_home(ddm: DashDataManager, filter_menu): #TODO test toggle
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
            
            filter_menu,
                    
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
            ),
            
            html.Div(id="statistic_tiles", style={"display": 'none'}),
            
        ], style={'backgroundColor':'#002552'}) #'background-image':'url("./assets/bed.jpg")'}
