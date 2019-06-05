import dash_auth
import random
import json
import dash
import dash_table
import numpy as np
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
df = pd.read_json('0_report.json')
df['datum'] = df['vreme'].str.split('T', expand=True)[0]
df['sati'] = df['vreme'].str.split('T', expand=True)[1].str.rstrip('Z')
df.drop(['vreme'], axis=1, inplace=True)

# app = dash.Dash(__name__)
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True
VALID_USERNAME_PASSWORD_PAIRS = [
    ['milos', 'milos']
]
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
access_token = 'pk.eyJ1Ijoia2ljbmkiLCJhIjoiY2p3aWV4OG8xMDM0cjN6bmMzdjR3cmlkbSJ9.0XZa71I57JD-ink0_qeHeQ'

people_list = [u'Miloš Nikić', u'Kristina Todorović', u'Nikola Nedeljković']

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(children=[
    html.H1(
        children="Projekat 'Analiza Buke'",
        style={
            'textAlign': 'left',

        }
    ),
    html.Div([html.Div([html.H1(""), ], style={'textAlign': "center"}),
              html.Div([html.Span("Izaberite Studenta", className="six columns",
                                  style={'textAlign': "left", "display": "block",
                                         "text-decoration": "none", "padding-top": 5, 'padding-bottom': 5, }), dcc.Dropdown(id="people-choice", options=[{'label': i, 'value': i} for i in people_list],
                                                                                                                            value=u'Miloš Nikić', className="six columns")],
                       className="row",
                       style={"display": "block", "margin-left": "auto",
                              "margin-right": "auto", "width": "80%", "padding-top": 10}),
              html.Div([dcc.Graph(id="my-graph")], className="row"),
              ], className="container"),
    html.P(id='placeholder'),
    html.Div(dcc.Graph(id='freq-plot')),
    html.Div([html.Label('Slider'),
              dcc.Slider(
        id='day-slider',
        min=0,

    )], id='output', style={'padding': 50}),

    dash_table.DataTable(id='my-table',
                         columns=[{'name': i, 'id': i} for i in ['_id', 'lat', 'lon', 'mac', 'naziv', 'opis', 'datum', 'sati']], row_selectable='multi')

])


@app.callback(
    Output("freq-plot", "figure"),
    [Input("my-table", "derived_virtual_data"),
     Input("my-table", "derived_virtual_selected_rows")])
def update_graph(rows, selected_rows):
    global df
    if selected_rows is None:
        selected_rows = []
    dff = df if rows is None else pd.DataFrame(rows)
    print(dff)
    print(selected_rows)

    traces = []
    for row in selected_rows:
        xaxis = []
        yaxis = []
        # Colors for traces
        r = str(random.randint(0, 255))
        g = str(random.randint(0, 255))
        b = str(random.randint(0, 255))
        for item in json.loads(dff.iloc[row, 1]):
            for x, y in item.items():
                xaxis.append(x)
                yaxis.append(y)
        trace = go.Scatter(x=xaxis, y=yaxis, name=str(dff.iloc[row, 0]), line=dict(
            width=2, color='rgb(' + r + ',' + g + ',' + b + ')'))
        traces.append(trace)
    layout = go.Layout(title='Frequency and Amplitude', hovermode='closest')
    return {'data': traces, 'layout': layout}


@app.callback(
    Output("my-graph", "figure"),
    [Input("day-slider", "value")])
def update_graph(value):
    global df
    if value is None:
        value = 0
    date = np.unique(df['datum'])[value]
    print(value)
    print(date)
    df_temp = df[df['datum'] == date]

    # print(df_temp.head())
    trace1 = [go.Scattermapbox(lat=df_temp["lat"], lon=df_temp["lon"], mode='markers', hoverinfo='none',
                               marker={'symbol': "circle", 'size': 8})]
    layout1 = go.Layout(title=f'Lokacije za snimanje', autosize=True, hovermode='closest', showlegend=False, height=550,
                        mapbox={'accesstoken': access_token, 'bearing': 0, 'center': {'lat': 44.80401, 'lon': 20.46513},
                                'pitch': 30, 'zoom': 12, "style": 'mapbox://styles/mapbox/light-v9'},   updatemenus=[
                              dict(
                                  buttons=([
                                      dict(
                                          args=[{
                                                'mapbox.zoom': 12,
                                                'mapbox.center.lon': '20.46513',
                                                'mapbox.center.lat': '44.80401',
                                                'mapbox.bearing': 0,

                                                }],
                                          label='Reset Zoom',
                                          method='relayout'
                                      )
                                  ]),
                                  direction='left',
                                  pad={'r': 0, 't': 0, 'b': 0, 'l': 0},
                                  showactive=False,
                                  type='buttons',
                                  x=0.45,
                                  xanchor='left',
                                  yanchor='bottom',
                                  bgcolor='#323130',
                                  borderwidth=1,
                                  bordercolor="#6d6d6d",
                                  font=dict(
                                      color="#FFFFFF"
                                  ),
                                  y=0.02
                              ),
                            dict(
                                  buttons=([
                                      dict(
                                          args=[{
                                                'mapbox.zoom': 13,
                                                'mapbox.center.lon': '20.4014404',
                                                'mapbox.center.lat': '44.8251851',
                                                'mapbox.bearing': 0,
                                                }],
                                          label='Studentska',
                                          method='relayout'
                                      ),
                                      dict(
                                          args=[{
                                                'mapbox.zoom': 13,
                                                'mapbox.center.lon': '20.4913788',
                                                'mapbox.center.lat': '44.8154327',
                                                'mapbox.bearing': 0,
                                                }],
                                          label='Bogoslovija',
                                          method='relayout'
                                      ),
                                      dict(
                                          args=[{
                                                'mapbox.zoom': 13,
                                                'mapbox.center.lon': '20.4756981',
                                                'mapbox.center.lat': '44.77187',
                                                'mapbox.bearing': 0,
                                                }],
                                          label='Jove Ilica',
                                          method='relayout'
                                      )]))])

    return {'data': trace1, 'layout': layout1}


@app.callback(
    [Output("my-table", "data"),
     Output("day-slider", "marks"),
     Output("day-slider", "max"),
     Output("my-table", "derived_virtual_selected_rows")],
    [Input("people-choice", "value"),
     Input("day-slider", "value")])
def setup_df(people, value):
    global df
    if value is None:
        value = 0
    if people == u'Miloš Nikić':
        df = pd.read_json('0_report.json')
    elif people == u'Kristina Todorović':
        df = pd.read_json('2_report.json')
    elif people == u'Nikola Nedeljković':
        df = pd.read_json('1_report.json')
    df['datum'] = df['vreme'].str.split('T', expand=True)[0]
    df['sati'] = df['vreme'].str.split('T', expand=True)[1].str.rstrip('Z')
    df.drop(['vreme'], axis=1, inplace=True)
    df_temp = df[df['datum'] == np.unique(df['datum'])[value]]
    return df_temp.to_dict('records'), {i: str(el) for i, el in enumerate(np.unique(df['datum']))}, len(np.unique(df['datum'])), []


if __name__ == '__main__':
    app.run_server(debug=True)
