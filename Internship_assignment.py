import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import json


df = pd.read_excel(r"C:\Users\divyanshu\Downloads\DAFebAssignment_RawData.xlsx")

app = dash.Dash()

app.layout = html.Div([
    html.Div([
        html.H1('Resolute AI Internship Dashboard', style={'textAlign': 'center'})
    ]),

    html.Br(),
    
    html.Div([
        html.H2('Welcome to the dashboard!'),
        html.H3('This dashboard displays the relationship between Activity Type & Room Number on the time series')], style={'topMargin':50})
    ,

    html.Div([
        html.H1("Room Number"),
        dcc.Dropdown(
            id='room_number',
            options=[
                {'label':'M1', 'value':'M1'},
                {'label':'M2', 'value':'M2'}
            ],
            value=['M1', 'M2'],
            multi=True
        )
    ]),

    html.Div([
        html.H2("Activity 1"),
        dcc.Dropdown(
            id='activity1',
            options=[
                {'label': 'True', 'value': True},
                {'label': 'False', 'value': False},
            ],
            value = [False, True],
            multi= True
        )
    ],style={'width':'48%', 'display':'inline-block'}
    ),

    html.Div([
        html.H2("Activity 2"),
        dcc.Dropdown(
            id='activity2',
            options=[
                {'label':'True', 'value':True},
                {'label':'False', 'value':False},
            ],
            value = [True, False],
            multi=True
        )
    ],style={'width':'48%',  'float':'right', 'display':'inline-block'}
    ),

    html.Div([
        dcc.Graph(
        id='graph')
    ], 
    style={'width':'50%', 'display':'inline-block'}
    ),

    html.Div([
        html.Pre(
            id='hover-data',
            style={'paddingTop':35}
        ),
        html.Pre(
            """
            We can see that Room M2 has more activity in comparison to Room M1.
            We also see that Activity 1 has more True flags for both the rooms.
            Another thing we notice is that activity in Room 1 is restricted to March 13.
            """
        )],
        style={'width':'30%', 'display':'inline-block','verticalAlign':'top'}
    )
    
])


@app.callback(
    Output('graph', 'figure'),
    [
        Input('room_number', 'value'),
        Input('activity1', 'value'),
        Input('activity2', 'value')
    ]
)
def plot_graph(room_number, activity1, activity2):
    data = []
    for i in room_number:
        data.append(go.Scatter(
        x=df['TimeStamp'],
        y=df[(df['Room Number'] == i) & (df['Activity 1'].isin(activity1)) & (df['Activity 2'].isin(activity2))]['No_of_Occupants'], 
        mode='markers',
        marker={
            'size':15,
            'opacity':0.7,
            'line': {'width': 0.5, 'color': 'white'}
        },
        name=i))
        
    layout = go.Layout(
        title='Room Number X Activity Type',
        xaxis={'title':"Timestamp"},
        yaxis={"title":"Occupants in room"},
        hovermode='closest'),
    

    return {'data':data, 'layout':layout}

@app.callback(
    Output('hover-data', 'children'),
    [Input('graph', 'hoverData')]
)
def callback_data(hoverData):
    return """
        Timestamp: {},
        Occupants in room: {}
        """.format(hoverData['points'][0]['x'], hoverData['points'][0]['y'])


if __name__ == '__main__':
    app.run_server()

        
