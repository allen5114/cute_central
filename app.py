import dash
from dash import Input, Output, State, html, dcc
import dash_bootstrap_components as dbc

import configparser

# youtube API
from apiclient.discovery import build
from youtube_api import YoutubeAPI

# import util scripts
from utils.button_utils import getClickedElementID
from utils.layout_utils import createVideoModal, createSearchFilterModel, createVideos, createVidColumns, createNavBar, createFooter
from youtube_api import getVidSearchKeywords

import flask

# Read configurations
config = configparser.ConfigParser()
config.read("./config/config.ini")

# grid dimensions
rows = int(config['GridDimension']['rows'])
columns = int(config['GridDimension']['columns'])

youtubeAPI = YoutubeAPI(config["Youtube"]["api_key"])
youtubeAPI.fake_search(rows * columns)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
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
    [Input("anchor-1", "n_clicks"), Input("anchor-2", "n_clicks"),
     Input("anchor-3", "n_clicks"), Input("anchor-4", "n_clicks"),
     Input("anchor-5", "n_clicks"), Input("anchor-6", "n_clicks"),
     Input("anchor-7", "n_clicks"), Input("anchor-8", "n_clicks"),
     Input("anchor-9", "n_clicks"), Input("anchor-10", "n_clicks"),
     Input("anchor-11", "n_clicks"), Input("anchor-12", "n_clicks")],
    [State("modal-fs", "is_open")],
)
def toggle_player_modal(n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, is_open):
    # update current video according to the clicked image anchor
    button_id = getClickedElementID()
    newOpenState = False
    
    clicked = False
    if n1 and button_id == "anchor-1":
       clicked = True
    elif n2 and button_id == "anchor-2":
       clicked = True
    elif n3 and button_id == "anchor-3":
       clicked = True
    elif n4 and button_id == "anchor-4":
       clicked = True
    elif n5 and button_id == "anchor-5":
       clicked = True
    elif n6 and button_id == "anchor-6":
       clicked = True
    elif n7 and button_id == "anchor-7":
       clicked = True
    elif n8 and button_id == "anchor-8":
       clicked = True
    elif n9 and button_id == "anchor-9":
       clicked = True
    elif n10 and button_id == "anchor-10":
       clicked = True
    elif n11 and button_id == "anchor-11":
       clicked = True
    elif n12 and button_id == "anchor-12":
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
    if button_id == "search_button":
        return True, createVidColumns(youtubeAPI, rows, columns)
    elif button_id == "search-topics-button":
        youtubeAPI.setQuery(checkedValues)
        youtubeAPI.search(rows * columns)
        return False, createVidColumns(youtubeAPI, rows, columns)
    return True, createVidColumns(youtubeAPI, rows, columns)
 

if __name__ == "__main__":
    app.run_server(debug=True, port=8000)