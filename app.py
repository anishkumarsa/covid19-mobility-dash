

import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go
import numpy as np
import re
from datetime import datetime as dt
from datetime import datetime
from dash.exceptions import PreventUpdate


import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table


app = dash.Dash(__name__, external_stylesheets=['assets/stylesheet.css'])
server=app.server

##################### Loading Data Frame####################################################################################


df=pd.read_csv('proc_global_mobility.csv')


##################### Data for dropdown ####################################################################################

l=list(df.country_region.value_counts().index)
l.sort()

cl=l #list of countries


# dict comphrehension list of sub region country wise
rl={i:list(df[(df['country_region']==i)&(df['type']=='r')]['sub_region_1'].value_counts().index) for i in cl}  
rl = {k:v for k,v in rl.items() if v for i in rl}

names = list(rl.keys())
nestedOptions = rl[names[0]]


#######################################################app layout################################################################

app.layout = html.Div([

############################################################### Title and Heading ####################################################  
    html.Div([
            html.Div(
                [
                    html.Div([
                        html.H1("COVID-19 MOBILITY DASHBOARD", style={'text-align': 'center','background': '#1abc9c','padding':'10px'}),
                        html.H2('Vizualization based on Google Mobility DataSet',style={'text-align': 'center','font-size':'20px'}),
                        html.P('''     Only if we end the COVID 19 everywhere can we end the pandemic anywhere. The entire world has the same goal: cases of COVID-19 need to go to zero.The below chart depicts
                            the mobility of different countries based on google mobility report and we updated only for countries which have complete data from 15/02/2020 onwards.'''),
                        html.P('''This new dataset from Google measures visitor numbers to specific categories of location (e.g. grocery stores; parks; train stations) every day and compares this change relative to 
                            baseline day before the pandemic outbreak. Baseline days represent a normal value for that day of the week, given as median value over the five‑week period from January 3rd to February 6th 2020. Measuring it relative to a normal value for that day of the week is helpful because people obviously often have different routines on weekends versus weekdays.'''),   
                    ]),#headings for the dashboard
                    html.Br()
                ]
            ),

############################################################### First Row #############################################################
            
            html.Div(
                [

                    ####################################First row Column 1 ############################
                    html.Div([

                        html.Br(),
                        html.H3('Global Mobility Choropleth',style={'text-align': 'left','font-size':'25px'}),

                        html.Div([
                            dcc.Dropdown(id="slct_wl",
                            options=[
                                {"label": "world","value": "world"},
                                {"label": "Asia","value": "asia"},
                                {"label": "Europe","value": "europe"},
                                {"label": "Africa","value": "africa"},
                                {"label": "North America","value": "north america"},
                                {"label": "South America","value": "south america"}],
                            multi=False,
                            value='world',
                            style={'width': "60%"}
                            ),
                            html.P('Select the region',style={'text-align': 'left','font-size':'10px'}),
                            dcc.Dropdown(id="slct_cat",
                            options=[
                                {"label": "retail & recreation","value": "retail & recreation"},
                                {"label": "grocery & pharmacy","value": "grocery & pharmacy"},
                                {"label": "parks","value": "parks"},
                                {"label": "transit station","value": "transit station"},
                                {"label": "workplace","value": "workplace"},
                                {"label": "residential","value": "residential"}],
                            multi=False,
                            value='retail & recreation',
                            style={'width': "60%"}
                            ), 
                            html.P('Select the category',style={'text-align': 'left','font-size':'10px'}),
                        html.Div(id='output_container1',children=[]),
                        ]), 

                        html.Br(),
                        html.Div(
                            [
                            dcc.Graph(id='my_bee_map1', figure={})      
                            ]),
                ], className= 'six columns'
                ),
                ####################################First row Column 2 ###############################
                    html.Div(
                        [   html.Br(),
                            html.Div([

                                html.H3('Countrywise Covid-19 Mobility Line Plot',style={'text-align': 'centre','font-size':'25px'}),
                                
                                dcc.Dropdown(id="slct_cntry",
                                    options=[{'label' : p, 'value' : p} for p in cl],
                                multi=False,
                                value="India",
                                style={'width': "60%"},
                                placeholder="Select a country",
                                ),
                            html.P('Select the Country to display the Line plots for different Mobility',style={'text-align': 'left','font-size':'10px'}),    
                            
                            html.Div(id='output_container',children=[]),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.P('',style={'text-align': 'left','font-size':'10px'}),
                            ]),
                            html.Div(
                            [
                            dcc.Graph(id='my_bee_map', figure={})      
                            ]),
                        ], className= 'six columns'
                    )
                ################################ First row Column 2 Ends ########################################

            ],className='row',style={'marginLeft': 10, 'marginRight': 10, 'marginTop': 10, 'marginBottom': 10,
           'backgroundColor':'#F7FBFE',
           'border': 'thin lightgrey dashed', 'padding': '4px 0px 10px 4px'}),  
            
    ],className='ten columns offset-by-one'
    ),
###############################################################Second Row#############################################################  
    html.Div([
            
            ####################################Second row Column 1 ############################
            html.Div([
                html.Div([
                    html.H3('Sub-Regionwise COVID-19 Mobility Line Plot and Mobility Change',style={'text-align': 'left','font-size':'25px'}),
                    dcc.Dropdown(id="name-dropdown",
                            options=[{'label' : p, 'value' : p} for p in names],
                        multi=False,
                        value = list(rl.keys())[0],
                        style={'width': "60%"},
                        placeholder="Select a country",
                        ),
                    html.P('Select the Country to choose sub region',style={'text-align': 'left','font-size':'10px'}),
                    
                    
                    dcc.Dropdown(id="opt-dropdown",
                        multi=False,
                        value='Huila Province',
                        style={'width': "60%"},
                        placeholder="Select a sub region",
                        ),
                    html.P('Select the sub region',style={'text-align': 'left','font-size':'10px'}),
                    dcc.Graph(id='my_bee_map2', figure={})
                ],className='six columns'),
                ####################################Second row Column 2 ############################
                html.Div([
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.H3('Variation in Mobilty  Percentage',style={'text-align': 'left','font-size':'20px'}),
                    html.P('Compare the mobility variation between two dates',style={'text-align': 'left','font-size':'10px'}),
                    html.P('Choose the dates to compare',style={'text-align': 'left','font-size':'10px'}),
                    dcc.DatePickerRange(
                        id='my-date-picker-range',
                        min_date_allowed=dt(2020, 2, 15),
                        max_date_allowed=dt(2020, 12, 30),
                        initial_visible_month=dt(2020, 2, 1),
                        clearable=False,
                        with_portal=True),
                    html.Br(),
                    html.Br(),
                    html.Br(),   
                    html.Div(id='output-container-date-picker-range'),
                    html.Div(id='table'),

                        ],className='five columns'),

            ],className='row',style={'marginLeft': 10, 'marginRight': 10, 'marginTop': 10, 'marginBottom': 10,
           'backgroundColor':'#F7FBFE',
           'border': 'thin lightgrey dashed', 'padding': '4px 0px 10px 4px'}),
            

    ],className='ten columns offset-by-one'),

############################################################### Third Row #############################################################






############################################## app Layout Ends ############################################################### 
    ]
    )


@app.callback(
    [Output(component_id='output_container1', component_property='children'),
    Output(component_id='my_bee_map1', component_property='figure')],
    [Input(component_id='slct_wl', component_property='value'),
     Input(component_id='slct_cat', component_property='value')]
)



def update_graph1(option_slctd,option_slctd1):
    
    container=" "
    dff=df.copy()
    dff = dff[dff['type']=='c']
    #if option_slctd!='oceania':
    fig = px.choropleth(data_frame=dff,  
                        locations='iso_alpha',   
                        color=option_slctd1, 
                        hover_name="country_region",
                        scope=option_slctd,
                        animation_frame='date',
                        animation_group='date',
                        color_continuous_scale='Plasma',
                        height=500,width=700,
                        )
    return container,fig

@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure')],
    [Input(component_id='slct_cntry', component_property='value')]
)


def update_graph(option_sltcd):
    dff=df.copy()
    if option_sltcd is None:
        container=" "
        dff = dff[dff['type']=='c']
        dff=dff[dff['country_region']=="India"]
        fig = px.line(dff, x="date", y=['retail & recreation','grocery & pharmacy','parks','transit station','workplace','residential'],height=500,width=740)
    else:
        container=" "
        dff = dff[dff['type']=='c']
        dff=dff[dff['country_region']==option_sltcd]
        fig = px.line(dff, x="date", y=['retail & recreation','grocery & pharmacy','parks','transit station','workplace','residential'],height=500,width=740)
    return container,fig  


@app.callback(
    Output('opt-dropdown', 'options'),
    [Input('name-dropdown', 'value')]
)
def update_date_dropdown(name):
    
    if name is None:
        s=rl['Angola']
        s.sort()
    else:
        s=rl[name]
        s.sort()
    return [{'label': i, 'value': i} for i in s]

  


    
@app.callback(
    Output(component_id='my_bee_map2', component_property='figure'),
    [Input('opt-dropdown', 'value'),
     Input('name-dropdown', 'value'),]
)

def update_graph2(selected_value,country_va):
    dff=df.copy()
    print(selected_value,country_va)
    
    try:
        dff=dff[(dff['country_region']==country_va)&(dff['type']=='r')&(dff['sub_region_1']==selected_value)]
        fig = px.line(dff, x="date", y=['retail & recreation','grocery & pharmacy','parks','transit station','workplace','residential'],height=500,width=700)
        return fig
    except KeyError:
        raise PreventUpdate

@app.callback(
    (Output('output-container-date-picker-range', 'children'),
    Output('table', 'children'),),
    [Input('opt-dropdown', 'value'),
    Input('name-dropdown', 'value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')]
)

def update_table(selected_value,selected_country,start_date,end_date):
    
    dff=df.copy()
    
    dff=dff[dff['country_region']==selected_country]
    s=rl[selected_country]

    if selected_value in s:

        if ((start_date is not None) and (end_date is not None)):
            dff=dff[(dff['country_region']==selected_country)&(dff['type']=='r')&(dff['sub_region_1']==selected_value)]
            print('ok')
            a=start_date
            b=end_date
            v1=dff[dff['date']==start_date] 
            v2=dff[dff['date']==end_date]

            print(v1)
            print(v2)

            v1=v1[v1.columns[5:13]]
            v2=v2[v2.columns[5:13]]

            print(v1)
            print(v2)

            if len(v1)==0:
                d1= {'date':[a],'retail & recreation':[0],'grocery & pharmacy':[0],'parks':[0],'transit station':[0],'workplace':[0],'residential':[0]}
                v1=pd.DataFrame(d1)
            if len(v2)==0:
                d2= {'date':[b],'retail & recreation':[0],'grocery & pharmacy':[0],'parks':[0],'transit station':[0],'workplace':[0],'residential':[0]}
                v2=pd.DataFrame(d2)

            v3=pd.concat([v1,v2])
            v3=v3.set_index(['date'])
            v3=v3.T    
            v3['absolute change']=v3[b]-v3[a]
            v3['index']=v3.index
            v3=v3[['index',a,b,'absolute change']]
            print(v3)
            t=html.Div(dash_table.DataTable(
                            data=v3.to_dict("records"),
                            columns=[{"id": x, "name": x} for x in v3.columns],page_size=10))
            string_prefix='selected date was '+str(a)+' and '+str(b)
            
            return string_prefix,t

        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True)
