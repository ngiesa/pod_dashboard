
from dash import dash_table
from conn.hdl.data_manager import DashDataManager
from dash import  html, dcc
import plotly.express as px

def build_filtered_master_table(ddm: DashDataManager, filter_condition={}):
    
    """ function for filtering and building front end master table """
    
    print("filter master")
        
    if filter_condition != {}:
        df_master = ddm.filter_main_table(filter_condition)
    
    if (len(list(filter_condition.values())) == 0):
        df_master = ddm.reset_filter()
        print("INIT DATA")
    
    if len(df_master) == 0:
        # if not data is returned for filter conditions
        print("no data for master table according to filters")
        return html.H1("No data to display", style={"padding": "40px"})

    df_master['RISK'] = df_master['RISK'].astype(float)
    
    return  dash_table.DataTable(data = df_master.to_dict('records'),
                                                     columns=[{"name": i, "id": i} for i in df_master.columns if i not in ["COPID",
                                                                                                                           "BEGANORG",
                                                                                                                           "ENDANORG", 
                                                                                                                           "BEGAWORG", 
                                                                                                                           "ENDAWORG"]], 
                                                     id='master_table_check',
                                                     cell_selectable=False,
                                                     page_size= 20,
                                                     style_as_list_view=True,
                                                     selected_rows=[],
                                                     row_selectable='single',
                                                        style_data = {
                                                            'whiteSpace': 'normal',
                                                            'textOverflow': 'ellipsis',
                                                            'width': 'auto',
                                                                
                                                            }, 
                                                        style_cell = {
                                                            'fontSize':16, 
                                                            'font-family':'sans-serif', 
                                                            'text-align': 'center',
                                                            'textOverflow': 'ellipsis',
                                                            'maxWidth': 400
                                                            },
                                                        style_data_conditional=[
                                                            {
                                                                'if': {
                                                                    'filter_query': '{RISK} >= 0.8',
                                                                    'column_id': 'RISK'
                                                                },
                                                                'backgroundColor': 'tomato',
                                                                'color': 'black'
                                                            },
                                                            {
                                                                'if': {
                                                                    'filter_query': '{RISK} > 0.4 && {RISK} < 0.8',
                                                                    'column_id': 'RISK'
                                                                },
                                                                'backgroundColor': '#FFA500',
                                                                'color': 'black'
                                                            },
                                                            {
                                                                'if': {
                                                                    'filter_query': '{RISK} <= 0.4',
                                                                    'column_id': 'RISK'
                                                                },
                                                                'backgroundColor': '#2E8B57',
                                                                'color': 'black'
                                                            },
                                                        ]
                                                    )
    
    
def build_details_main_view(ddm: DashDataManager, index):
    
    """ build detail views with vital signs per patient """
    
    op_item = ddm.display_master_table.iloc[index]
    c_op_id = op_item["COPID"]
    c_begin = op_item["BEGANORG"]
    c_end = op_item["ENDANORG"]
    
    hover_data = {"c_time": "|%B %d, %Y"}
    x = "c_time"
    
    op_master = ddm.data_op_master[["c_op_id", "c_root_id"]]
    c_root = op_master[op_master.c_op_id == c_op_id]["c_root_id"].iloc[0]
    df_vitals = ddm.get_vitals(c_root=c_root, c_begin=c_begin, c_end=c_end)
    
    df_plot = df_vitals.groupby(["c_time", "var_name"])["c_value"]\
            .mean().reset_index().pivot(columns="var_name", index="c_time", values="c_value").reset_index()
            
    if len(df_plot) == 0:
        print("vitals for patient not found")
        return html.H1("No charts to display", style={"padding": "40px"})
    
    plot_cols = list(df_plot.columns)
    print(plot_cols)
    
    title_bp = ""
    
    if "vital_nipb_sys" in plot_cols:
        y_bp = ["vital_nipb_sys", "vital_nipb_dia"]
        title_bp = title_bp + "Non-Invasive Blood Pressure"
    elif "vital_ibp" in plot_cols:
        y_bp = ["vital_ibp_sys", "vital_ibp_dia"]
        title_bp = title_bp + "Invasive Blood Pressure"
    else:
        y_bp = None
    
    print(y_bp)
    
    fig_blood_pressure = px.scatter(
            df_plot.reset_index(), 
            x=x, 
            y=y_bp,
            hover_data=hover_data,
            title=title_bp,
            color_discrete_sequence=['red', 'darkred']
            )
    
    title_puls = "Pulse / Heart Rate"
    y_pul = []
    if "vital_puls" in plot_cols:
        y_pul = y_pul + ["vital_puls"]
    if "vital_hr" in plot_cols:
        y_pul = y_pul + ["vital_hr"]
    if ("vital_hr" not in plot_cols) & ("vital_puls" not in plot_cols):
        y_pul = None
    
    fig_pulse = px.scatter(
            df_plot.reset_index(), 
            x=x, 
            y=y_pul,
            hover_data=hover_data,
            title=title_puls,
            color_discrete_sequence=['lightgreen', 'cyan']
            )
    
    title_spo2 = "Blood Oxygen Saturation"
    if "vital_spo2" in plot_cols:
        y_spo2 = ["vital_spo2"]
    else:
        y_spo2 = None
    
    fig_spo2 = px.scatter(
            df_plot.reset_index(), 
            x=x, 
            y=y_spo2,
            hover_data=hover_data,
            title=title_spo2,
            color_discrete_sequence=['blue']
            )
    

    title_rr = "Respiratory Rate"
    if "vital_rr" in plot_cols:
        y_rr = ["vital_rr"]
    else:
        y_rr = None
        
    
    data_frame = df_plot.reset_index() 
    x = "c_time"

    fig_rr = px.scatter(
                data_frame=data_frame,
                x=x, 
                y=y_rr,
                hover_data=hover_data,
                title=title_rr,
                color_discrete_sequence=['yellow']
                )
    
    
    for fig in [fig_pulse, fig_blood_pressure, fig_spo2, fig_rr]:
        fig.update_layout(showlegend=True, 
                            xaxis_title=None, 
                            yaxis_title=None, 
                            plot_bgcolor='#F5F5F5',
                            title_font_family="sans-serif",
                            margin=dict(l=40, r=20, t=50, b=10),
                            height=340,
                            legend=dict( 
                                orientation="h", 
                                bgcolor='white',
                                x=0.60
                                ),
                            legend_title=None
                            )
        
        
        fig.update_traces(marker=dict(size=8,
                              line=dict(width=1)),
                  selector=dict(mode='markers'))
        
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='grey')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='grey')
        
    style={'width': '50%', 'height': '100%', 'display': 'inline-block', 'padding-top': '0px', 'background-color': "white"}
    
    return   html.Div(
        className='row_1', children=[
            html.Div(
                children=[
                    dcc.Graph(className="vital-graphs", figure=fig_blood_pressure, style=style,  config={'displayModeBar': False}) if y_bp is not None else None,
                    dcc.Graph(className="vital-graphs", figure=fig_pulse, style=style, config={'displayModeBar': False}) if y_pul is not None else None,
                    ], style={'background-color': 'white', 'padding-top': '5px'}
                ),
            html.Div(
                children=[
                    dcc.Graph(className="vital-graphs", figure=fig_spo2, style=style,  config={'displayModeBar': False}) if y_spo2 is not None else None,
                    dcc.Graph(className="vital-graphs", figure=fig_rr, style=style, config={'displayModeBar': False}) if y_rr is not None else None,
                    ], style={ 'background-color': 'white'}
                )
            ], 
            style={'padding-top': '0px',}
        )
    
