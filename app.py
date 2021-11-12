import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# import util scripts
from utils.button_utils import getClickedButtonID
from utils.layout_utils import getVidIframe
from youtube_api import getVidSearchKeywords, searchVids

app = dash.Dash(__name__)
app.title = 'Cute Central'

app.layout = html.Div(
    children=[
        html.H1(children="Cute Central",),
        html.Button('puppy', id='puppy-button'),
        html.Button('kitten', id='kitten-button'),
        html.Div(id='video-list')
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
    return html.Div(children=[getVidIframe(url) for url in searchVids(keywords)])

if __name__ == "__main__":
    app.run_server(debug=True, port=8000)