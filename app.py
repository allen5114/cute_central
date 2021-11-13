import dash
from dash import Input, Output, State, html, dcc
import dash_bootstrap_components as dbc

import configparser

# youtube API
from apiclient.discovery import build
from youtube_api import YoutubeAPI

# import util scripts
from utils.button_utils import getClickedElementID
from utils.layout_utils import createVidButton, createVideoModal
from youtube_api import getVidSearchKeywords

import flask

# Read configurations
config = configparser.ConfigParser()
config.read("./config/config.ini")

youtubeAPI = YoutubeAPI(config["Youtube"]["api_key"])
youtubeAPI.fake_search()

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Cute Therapy'

app.layout = dbc.Container(
    [
        html.H1(children="Cute Therapy", style= {'textAlign':'center', 'marginTop':40, 'marginBottom': 40}),
        html.Button('puppy', id='puppy-button'),
        html.Button('kitten', id='kitten-button'),
        html.Div(id='video-list', style={'textAlign':'center'}),
        html.Div(id='img-list', style={'textAlign':'center'}),
        createVideoModal(youtubeAPI),
        createVidButton('anchor-1', youtubeAPI.getThumbnail(0)),
        createVidButton('anchor-2', youtubeAPI.getThumbnail(1))
    ]
)


## Callback upon a category button click
#@app.callback(Output('video-list', 'children'),
#              [Input('puppy-button', 'n_clicks'),
#              Input('kitten-button', 'n_clicks')]
#)
#def category_clicked(btn1, btn2):
#    button_id = getClickedElementID()
#    keywords = getVidSearchKeywords(button_id)
#    return html.Div(children=[getVidIframe(url) for url in youtubeAPI.search(keywords)])


## Callback upon a category button click
#@app.callback(Output('img-list', 'children'),
#              [Input('puppy-button', 'n_clicks'),
#              Input('kitten-button', 'n_clicks')]
#)
#def category_clicked2(btn1, btn2):
#    button_id = getClickedElementID()
#    keywords = getVidSearchKeywords(button_id)
#    urls, thumbnails = youtubeAPI.search2(keywords)
#    return html.Div(children=[createVidButton(url) for url in thumbnails])

# Open a modal and auto play video on image anchor click
@app.callback(
    [Output("modal-fs", "is_open"), Output("player", "children")],
    [Input("anchor-1", "n_clicks"), Input("anchor-2", "n_clicks")],
    [State("modal-fs", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    # update current video according to the clicked image anchor
    button_id = getClickedElementID()
    newOpenState = is_open
    if button_id != None:
        tokens = button_id.split('-')
        if tokens[0] == 'anchor':
            youtubeAPI.setCurrentVid(int(tokens[1])-1)
            newOpenState = not is_open
    
    # Update iframe source
    playerChildren = [html.Iframe(src=youtubeAPI.getCurrentUrl(),
                       width="90%",
                       height="90%",
                       allow="autoplay"
    )]
    return newOpenState, playerChildren
 

if __name__ == "__main__":
    app.run_server(debug=True, port=8000)