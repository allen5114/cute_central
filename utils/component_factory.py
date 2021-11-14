import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc

# Create a clickable/anchored image
def getImageAnchor(node_id, css_class_name, src_url):
    return html.A(id=node_id, children=[html.Img(className=css_class_name, src=src_url)])

# Create a clickable/anchored video
def getVideoAnchor(nodeId, imgUrl):
    return html.Div(className='video-list-item', children=[
        html.A(className='video-anchor', id=nodeId, children=[
            html.Img(className='video-thumbnail', src=imgUrl),
            html.Img(className="video-play", src='/assets/images/play.png')
        ])
    ])

# Create a modal
def getModal(modal_id, modal_body_id, full_screen, modal_children):
    return html.Div(
        children=[
            dbc.Modal(
                children=[
                    dbc.ModalHeader(dbc.ModalTitle("")),
                    dbc.ModalBody(
                        id=modal_body_id, 
                        children=modal_children
                    ),
                ],
                id=modal_id,
                fullscreen=full_screen,
                style={'textAlign':'center'}
            ),
        ]
    )