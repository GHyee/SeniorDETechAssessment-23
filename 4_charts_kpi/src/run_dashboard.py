import dash
from dash import dcc
from dash import html
import requests
import pandas as pd
from dash.dependencies import Input, Output


# Set default start and end dates
DEFAULT_FROM_DATE = "2022-01-01T00:00:00Z"
DEFAULT_TO_DATE = "2023-01-01T00:00:00Z"

# Define function to get data from API
def get_data(from_date, to_date):
    url = f"https://api.covid19api.com/live/country/singapore/status/confirmed?from={from_date}&to={to_date}"
    response = requests.get(url)
    data = pd.DataFrame(response.json())
    return data

# Initialize the app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.Label("From:"),
    dcc.Input(
        id='from-date',
        type='text',
        value=DEFAULT_FROM_DATE,
        style={'width': '100%'}
    ),
    html.Label("To:"),
    dcc.Input(
        id='to-date',
        type='text',
        value=DEFAULT_TO_DATE,
        style={'width': '100%'}
    ),
    dcc.Graph(id='cases-graph')
])

# Define the callback to update the graph
@app.callback(Output('cases-graph', 'figure'),
              [Input('from-date', 'value'), Input('to-date', 'value')])
def update_graph(from_date, to_date):
    data = get_data(from_date, to_date)
    figure = {
        'data': [{
            'x': data['Date'],
            'y': data['Confirmed'],
            'type': 'line',
            'name': 'Confirmed Cases'
        }],
        'layout': {
            'title': 'COVID-19 Confirmed Cases in Singapore',
            'xaxis': {'title': 'Date', 'tickmode': 'linear', 'tick0': 0, 'dtick': 'M1', 'tickformat': '%b %Y'},
            'yaxis': {'title': 'Number of Cases'}
        }
    }
    return figure


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
