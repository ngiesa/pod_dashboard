from dash import dcc
from dash import html
from datetime import date
from conn.hdl.data_manager import DashDataManager
import dash_bootstrap_components as dbc

import dash_daq
from dash import Dash, dcc, html, Input, Output, callback, dash_table
import pandas as pd
from sidebar.view_builder import build_filtered_master_table
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff

def build_pod_trend_line(ddm: DashDataManager):
    if ddm.display_master_table is None:
        ddm.filter_main_table({})
    fig = px.bar(ddm.df_nudesc_master.merge(ddm.display_master_table.rename(columns={"COPID":"c_op_id"})\
        [["c_op_id"]], on="c_op_id").groupby(["day", "pod"])["c_op_id"]\
            .count()\
            .reset_index()\
            .rename(columns={"c_op_id": "#surgeries"}), 
            x='day', y="#surgeries",
            hover_data=['pod'], color='pod',
            labels={"#surgeries":"#surgeries"}, 
            height=400, title="POD Progression over Days ({} prevalence)".format(ddm.pod_revalence))
    return fig

#TODO include filter conditions here as well callback??? MAYBE INCLUDE MORE IN FILTER CALLBACKS??? 
# https://community.plotly.com/t/bug-input-not-triggering-callback/13631
#TODO MAYBE LAYOUT IS NOT REGISTERED???

def build_age_distribution(ddm: DashDataManager):
    if ddm.display_master_table is None:
        ddm.filter_main_table({})
    fig_age = px.histogram(ddm.display_master_table, x="AGE", color="POD", marginal='box', title="Distribution POD", hover_data = "POD", barmode="relative")
    fig_age.update_layout(bargap=0.03, height=400) #width=600, height=400,
    return fig_age

def build_gender_distribution(ddm: DashDataManager):
    if ddm.display_master_table is None:
        ddm.filter_main_table({})
    fig_gender = px.bar(ddm.display_master_table.groupby(["SEX", "POD"])["BEGAN"].count().reset_index()\
            .rename(columns={"BEGAN": "#surgeries"}), x="POD", y="#surgeries", color="SEX",  height=400) #TODO
    return fig_gender
    

def build_stats(ddm: DashDataManager):
    return html.Div(children=[ dcc.Graph(
                        id="pod_progression",
                        config={"displayModeBar": False},
                        figure=build_pod_trend_line(ddm=ddm)
                        ), 
                    dbc.Row([
                            dbc.Col([
                                dcc.Graph(
                                    id="age_distribution",
                                    config={"displayModeBar": False},
                                    figure=build_age_distribution(ddm)
                                    ), 
                            ],),
                            dbc.Col([
                                dcc.Graph(
                                    id="gender_distribution",
                                    config={"displayModeBar": False},
                                    figure=build_gender_distribution(ddm)
                                    ), 
                            ],)
                        ]), 
    ])   

def render_statistics(ddm: DashDataManager, filter_menu):
    return html.Div( 
        children=[
            html.Div(
                children=[ 
                    html.Div(
                        children=[
                            html.H1(
                                children="Postoperative Delirium Cockpit", className="header-title"
                            ),
                            html.P(
                                children=(
                                    "Insights Statistics Cohort"
                                ),
                                className="header-description",
                            ),   
                        ],
                        className="header"
                    ),
                    
                    filter_menu,
                    
                    html.Div(id="statistic_tiles", children=[build_stats(ddm=ddm)]),
                    
                    html.Div(
                            id="master_table_content",
                            className = "master-table-content",
                            children=[build_filtered_master_table(ddm=ddm, filter_condition={})],
                            style={'display': 'none'}
                                    ),
                    
                ],
                className="background",
                style={'backgroundColor':'#002552'}     
            ),]
        )
    
    
    