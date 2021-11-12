import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
#from dash import Dash, html, Input, Output, callback_context

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

# Get the ID of the last clicked category button
def getClickedButtonID():
    ctx = dash.callback_context
    if not ctx.triggered:
        return None
    else:
        return ctx.triggered[0]['prop_id'].split('.')[0]

# Callback upon a category button click
@app.callback(Output('video-list', 'children'),
              [Input('puppy-button', 'n_clicks'),
              Input('kitten-button', 'n_clicks')]
)
def category_clicked(btn1, btn2):
    button_id = getClickedButtonID()
    return html.Div([html.Span(children=button_id )])

if __name__ == "__main__":
    app.run_server(debug=True, port=8000)