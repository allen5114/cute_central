import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

# Helper function to create a clickable image anchor
def createVidButton(elementId, imgUrl):
    return html.Div(className='video-list-item', children=[
        html.A(className='video-anchor', id=elementId, children=[
            html.Img(className='video-thumbnail', src=imgUrl),
            html.Img(className="video-play", src='/assets/images/play.png')
        ], href='#')
    ])

# Helper function to create a modal that embeds a video
def createVideoModal(youtubeAPI):
    return html.Div(
        children=[
            dbc.Modal(
                children=[
                    dbc.ModalHeader(dbc.ModalTitle("")),
                    dbc.ModalBody(
                        id='player', 
                        children=[html.Iframe(src=youtubeAPI.getCurrentUrl(),
                            width="90%",
                            height="90%",
                            allow="autoplay")
                        ]
                    ),
                ],
                id="modal-fs",
                fullscreen=True,
                style={'textAlign':'center', 'background-color':'rgba(200,200,200,0.1)'}
            ),
        ],style={'background-color':'rgba(200,200,200,0.1)'}
    )