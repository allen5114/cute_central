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

#externalScripts= ['https://www.youtube.com/iframe_api']

app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.BOOTSTRAP], 
#                external_scripts=externalScripts,
                update_title=None,
                meta_tags=[{'name': 'viewport',
                           'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5'}])
app.title = 'Cute Central'

server = app.server

app.layout = html.Div(
    [
        createNavBar(),
#        html.Button(id='test', children=["test"]),
#        html.Div(id="iframe-player2"),
        createVideoModal(youtubeAPI),
        createSearchFilterModel(youtubeAPI),
        createVideos(youtubeAPI, int(config['GridDimension']['rows']), int(config['GridDimension']['columns'])),
        createFooter(),
    ]
)

# Open terms of use
@app.callback (
    Output("terms-modal", "is_open"),
    Input("terms_of_use_button", "n_clicks")
)
def open_terms_of_use(n_clicks):
    if n_clicks:
        return True
    return False

#Open Privacy Policy
@app.callback (
    Output("privacy-policy-modal", "is_open"),
    Input("privacy-policy-button", "n_clicks")
)
def open_privacy_policy(n_clicks):
    if n_clicks:
        return True
    return False


# Open a modal and auto play video on image anchor click
@app.callback(
    [Output("modal-fs", "is_open"), Output("iframe-player", "src")],
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
        return True, youtubeAPI.getCurrentUrl()
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
        import waitress
        import logging
        logger = logging.getLogger('waitress')
        logger.setLevel(logging.INFO)
        waitress.serve(server, host='0.0.0.0', port=80)