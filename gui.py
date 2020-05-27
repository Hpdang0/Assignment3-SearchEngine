'''
This .py file contains all of the dash core components that are used in the MAGIC Filter Configuration GUI
'''
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import requests
import uuid
import os

from collections import defaultdict
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


default = 'ENTER HERE'


external_stylesheets = [
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
    "/assets/style.css",
]
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=external_stylesheets,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
server = app.server

# BEGIN ADDING THE ELEMENTS OF THE GUI ------------------
app.layout = dbc.Container([html.Div([

                html.H1('CHTH Search Engine'), # this is the title

                html.Div(id='output-DFT_WIN',
                         children='Enter a value and press submit',
                         style= {'background-color': 'white'}),

                html.Div(dcc.Input(id='input-DFT_WIN', type='text', value=default),style={'margin-bottom': 15}),

                html.Button('Enter', id='enter_button'),

                html.Div(id='output-search',
                         children='push enter when ready',
                         style= {'background-color': 'white'}),


], style={'columnCount': 1})])  # for the whole div


# APP CALLBACKS BEGIN -------------------------------------------------------
# DFT_WIN_NUM_SAMPLES_LOG2 UPDATE IS HERE ------

@app.callback(
    dash.dependencies.Output('output-DFT_WIN', 'children'),
    [dash.dependencies.Input('input-DFT_WIN', 'value')])
def update_dft(value):
    """Updating the DFT_WIN_NUM_SAMPLES VARIABLE"""
    global default
    default = value
    # HERE WE COULD CHECK ERRORS for the input text
    
    return f'Searching: "{value}".'


@app.callback(
    dash.dependencies.Output('output-search', 'children'),
    [dash.dependencies.Input('enter_button', 'n_clicks')])
def update_protect_num_bins(n_clicks):
    #global protect_num_bins
    #protect_num_bins = value
    if n_clicks is None:
        n_clicks = 0
    
    if n_clicks == 0:
        return f'push enter when ready'

    #search the contents of default
    return f'SEARCHING FOR: "{default}""!'

# -----------------------------------------------------------------generic defs for conversions from hardware to software

if __name__ == "__main__":
    app.run_server(debug=True)