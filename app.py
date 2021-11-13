import dash
from dash import Input, Output, State, html
import dash_bootstrap_components as dbc

import configparser

# youtube API
from apiclient.discovery import build
from youtube_api import YoutubeAPI

# import util scripts
from utils.button_utils import getClickedButtonID
from utils.layout_utils import getVidIframe
from youtube_api import getVidSearchKeywords

# Read configurations
config = configparser.ConfigParser()
config.read("./config/config.ini")

youtubeAPI = YoutubeAPI(config["Youtube"]["api_key"])

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Cute Central'

videoModal = html.Div(
    children=[
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("")),
                dbc.ModalBody(html.Iframe(src='https://www.youtube.com/embed/C9OMAX91oyw',
                       width="90%",
                       height="90%"
                )),
            ],
            id="modal-fs",
            fullscreen=True,
            style={'textAlign':'center', 'background-color':'rgba(200,200,200,0.1)'}
        ),
    ],style={'background-color':'rgba(200,200,200,0.1)'}
)

app.layout = dbc.Container(
    [
        html.H1(children="Cute Central", style= {'textAlign':'center', 'marginTop':40, 'marginBottom': 40}),
        html.Button('puppy', id='puppy-button'),
        html.Button('kitten', id='kitten-button'),
        dbc.Button('modal', id='modal-button'),
        html.Div(id='video-list', style={'textAlign':'center'}),
        videoModal,
    ]
)


# Callback upon a category button click
@app.callback(Output('video-list', 'children'),
              [Input('puppy-button', 'n_clicks'),
              Input('kitten-button', 'n_clicks')]
)
def category_clicked(btn1, btn2):
    button_id = getClickedButtonID()
    keywords = getVidSearchKeywords(button_id)
    return html.Div(children=[getVidIframe(url) for url in youtubeAPI.search(keywords)])

# Open a modal and auto play video
@app.callback(
    Output("modal-fs", "is_open"),
    [Input("modal-button", "n_clicks")],
    [State("modal-fs", "is_open")],
)
def toggle_modal(n, is_open):
    if n:
        return not is_open
    return is_open

if __name__ == "__main__":
    app.run_server(debug=True, port=8000)