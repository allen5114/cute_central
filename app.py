import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

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

app = dash.Dash(__name__)
app.title = 'Cute Central'

app.layout = html.Div(
    children=[
        html.H1(children="Cute Central", style= {'textAlign':'center', 'marginTop':40, 'marginBottom': 40}),
        html.Button('puppy', id='puppy-button'),
        html.Button('kitten', id='kitten-button'),
        html.Div(id='video-list', children=[]    
        ,style={'display': 'inline-block', 'width': '75%', 'verticalAlign': 'top', 'textAlign':'center'})
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

if __name__ == "__main__":
    app.run_server(debug=True, port=8000)