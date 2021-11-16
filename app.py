import dash
from dash import Input, Output, State, html, dcc, MATCH, ALL
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

import configparser

# youtube API
from apiclient.discovery import build
from youtube_api import YoutubeAPI

# import util scripts
from utils.button_utils import getClickedElementID
from utils.layout_utils import createVideoModal, createSearchFilterModel, createVideos, createVidColumns, createNavBar, createFooter
from youtube_api import getVidSearchKeywords

#import flask
import json

import argparse

# Read configurations
config = configparser.ConfigParser()
config.read("./config/config.ini")

# grid dimensions
rows = int(config['GridDimension']['rows'])
columns = int(config['GridDimension']['columns'])

youtubeAPI = YoutubeAPI(config["Youtube"]["api_key"])
youtubeAPI.fake_search(rows * columns)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], update_title=None,
                meta_tags=[{'name': 'viewport',
                           'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5'}])
app.title = 'Cute Central'

app.layout = html.Div([dbc.Container(
    [
        createNavBar(),
        createVideoModal(youtubeAPI),
        createSearchFilterModel(youtubeAPI),
        createVideos(youtubeAPI, int(config['GridDimension']['rows']), int(config['GridDimension']['columns'])),
        createFooter(),
    ]
)])

# Open a modal and auto play video on image anchor click
@app.callback(
    [Output("modal-fs", "is_open"), Output("player", "children")],
    [Input({'type': 'video-anchor', 'index': ALL}, 'n_clicks')],
    prevent_initial_call=True,
)
def toggle_player_modal(n_clicksAll):
    # check if any video-anchor type element was clicked on
    typeClicked = False
    for n in n_clicksAll:
        if n != None:
            typeClicked = True
    
    # update the current video's iframe src
    if typeClicked:
        button_idDict = json.loads(getClickedElementID())  
        youtubeAPI.setCurrentVid(button_idDict["index"])
        playerChildren = [html.Iframe(src=youtubeAPI.getCurrentUrl(),
                           width="90%", height="90%", allow="autoplay"
        )]
        return True, playerChildren
    raise PreventUpdate

# Search and update the list of videos
@app.callback (
    Output("videos", "children"),
    Input("search-topics-button", "n_clicks"),
    [State("search-checklist", "value"),
     State("sortby-options", "value")],
    prevent_initial_call=True
)
def search_and_update_videos(n_clicks, pickedAnimals, sortByValue):
    if n_clicks != None:
        youtubeAPI.setQuery(pickedAnimals)
        youtubeAPI.setOrder(sortByValue)
        youtubeAPI.search(rows * columns)
        return createVidColumns(youtubeAPI, rows, columns)
    raise PreventUpdate

# Handle Search modal's open and close events
@app.callback(
    Output("search-filter-modal", "is_open"),
    [Input("search_button", "n_clicks"),
     Input("search-topics-button", "n_clicks")],
    prevent_initial_call=True
)
def toggle_search_modal(n_clicks, n_clicks2):
   button_id = getClickedElementID()
   if button_id == "search_button":
       return True
   elif button_id == "search-topics-button":
       return False
   raise PreventUpdate

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("runMode", help="Use 0 for Development and 1 for Production")
    args = parser.parse_args()
    if args.runMode == "0":
        app.run_server(debug=True, port=8000)
    elif args.runMode == "1":
        app.run_server(debug=False, port=80, host='0.0.0.0')