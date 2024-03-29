import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc

# Create a clickable/anchored image
def getImageAnchor(node_id, css_class_name, src_url):
    return html.A(id=node_id, children=[html.Img(className=css_class_name, src=src_url)])

# Create a clickable/anchored video
def getVideoAnchor(nodeId, imgUrl):
    return html.Div(className='video-container-inner', children=[
        html.A(className='video-anchor', id=nodeId, children=[
            html.Img(className="video-play", src='/assets/images/play.png'),
            html.Img(className='video-thumbnail', src=imgUrl)
        ])
    ])

# Create a modal
def getModal(modal_id, modal_body_id, full_screen, modal_header, modal_children, modal_footer):
    return html.Div(
        children=[
            dbc.Modal(
                children=[
                    modal_header,
                    dbc.ModalBody(
                        id=modal_body_id, 
                        children=modal_children,
                        style={'paddingLeft':'20', 'paddingRight':'20', 'textAlign':'center'}
                    ),
                    modal_footer
                ],
                id=modal_id,
                fullscreen=full_screen,
                centered=True,
                style={'textAlign':'center'}
            ),
        ]
    )