import re
import time

import tokenizer
import search


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import requests
import uuid
import os
from collections import defaultdict
import dash_bootstrap_components as dbc

_QUERY_LEGAL = re.compile(r'^[a-z|A-Z|\d| ]+$')



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
                         children= 'press enter when ready',#'push enter when ready',
                         style= {'background-color': 'white', "white-space": "pre-wrap"},),


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
    global default
    #protect_num_bins = value
    if n_clicks is None:
        n_clicks = 0
    
    if n_clicks == 0:
        return f'push enter when ready'

    if not ensure_legal(default):
        return f'ERROR, {default} IS NOT ALPHANUMERIC'

    # Tokenize just like how we did for indexing
    query_tokens = tokenizer.tokenize_query(default)

    # Time and do search
    start = time.time()
    results = search.search(query_tokens)
    end = time.time()
    the_time = '[Query took {:.3f} seconds]'.format(end - start)
    
    # Print the results
    nl = '\n'
    # answers = []
    # for url in results:
    #     answers.append('<a href="#">' + url + '</a>')
    
    #search the contents of default
    # return f'SEARCHED FOR: "{default}"!{nl}{answers}{nl}{the_time}{nl}'
    return f"Search results:{nl}{nl}{nl.join(results)}{nl}{the_time}"

#-------------------------------------------------------------------------------------

def ensure_legal(i: str) -> bool:
    if _QUERY_LEGAL.search(i) == None:
        return False
    return True

if __name__ == '__main__':
    max_doc_id = 0
    with open("final.ids", 'r', encoding='utf-8') as file:
        first_line = file.readline()
        for last_line in file:
            pass
    lis = last_line.split(' ', 1)
    max_doc_id = int(lis[0])
    tokenizer = tokenizer.Tokenizer()
    search = search.Search('final.index', 'final.ids', max_doc_id)
    app.run_server(debug=True)
