import dash
from dash import Input, Output, State, html, dcc
import dash_bootstrap_components as dbc

import configparser

# youtube API
from apiclient.discovery import build
from youtube_api import YoutubeAPI

# import util scripts
from utils.button_utils import getClickedElementID
from utils.layout_utils import createVidButton, createVideoModal, createSearchFilterModel, createVideos, createVidColumns, createNavBar, createFooter
from youtube_api import getVidSearchKeywords

import flask

# Read configurations
config = configparser.ConfigParser()
config.read("./config/config.ini")

youtubeAPI = YoutubeAPI(config["Youtube"]["api_key"])
youtubeAPI.fake_search()

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Cute Therapy'

app.layout = html.Div([dbc.Container(
    [
        createNavBar(),
        html.Button('puppy', id='puppy-button'),
        html.Button('kitten', id='kitten-button'),
        html.Div(id='video-list', style={'textAlign':'center'}),
        createVideoModal(youtubeAPI),
        createSearchFilterModel(youtubeAPI),
        createVideos(youtubeAPI, 3),
        createFooter(),
    ]
)])

# Compose a query from checked filters
def getQuery(checkedValues):
    query = ""
    if len(checkedValues) > 0:
        query = "cute"
        for value in checkedValues:
            query = query + " | " + value;
    else:
        query = "cute animals"
    return query;
    
# Open a modal and auto play video on image anchor click
@app.callback(
    [Output("modal-fs", "is_open"), Output("player", "children")],
    [Input("anchor-1", "n_clicks"), Input("anchor-2", "n_clicks"),
     Input("anchor-3", "n_clicks"), Input("anchor-4", "n_clicks"),
     Input("anchor-5", "n_clicks"), Input("anchor-6", "n_clicks")],
    [State("modal-fs", "is_open")],
)
def toggle_player_modal(n1, n2, n3, n4, n5, n6, is_open):
    # update current video according to the clicked image anchor
    button_id = getClickedElementID()
    newOpenState = False
    
    clicked = False
    if n1 and button_id == "anchor-1":
       clicked = True
    if n2 and button_id == "anchor-2":
       clicked = True
    if n3 and button_id == "anchor-3":
       clicked = True
    if n4 and button_id == "anchor-4":
       clicked = True
    if n5 and button_id == "anchor-5":
       clicked = True
    if n6 and button_id == "anchor-6":
       clicked = True
       
    if clicked:
        tokens = button_id.split('-')
        if tokens[0] == 'anchor':
            youtubeAPI.setCurrentVid(int(tokens[1])-1)
            newOpenState = True
    
    # Update iframe source
    playerChildren = [html.Iframe(src=youtubeAPI.getCurrentUrl(),
                       width="90%",
                       height="90%",
                       allow="autoplay"
    )]
    print("open model " + str(newOpenState))
    return newOpenState, playerChildren

# Open a modal for search filter
@app.callback(
    [Output("search-filter-modal", "is_open"),
     Output("videos", "children")],
    [Input("search_button", "n_clicks"),
     Input("search-topics-button", "n_clicks"),
     Input("search-checklist", "value")],
    [State("search-filter-modal", "is_open")],
)
def toggle_search_modal(n_clicks, n_clicks2, checkedValues, is_open):
    button_id = getClickedElementID()
    rows = 3
    if button_id == "search_button":
        return True, createVidColumns(youtubeAPI, rows)
    elif button_id == "search-topics-button":
        query = getQuery(checkedValues)
        youtubeAPI.search(query)
        return False, createVidColumns(youtubeAPI, rows)
    return True, createVidColumns(youtubeAPI, rows)
 

if __name__ == "__main__":
    app.run_server(debug=True, port=8000)