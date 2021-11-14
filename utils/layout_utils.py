import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

# Create navigation bar
def createNavBar():
    navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src='/assets/images/icon.png', height="30px")),
                        dbc.Col(dbc.NavbarBrand("Cute Central", className="logo-text")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="#",
                style={"textDecoration": "none"},
            ),
#            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
#            dbc.Collapse(
#                search_bar,
#                id="navbar-collapse",
#                is_open=False,
#                navbar=True,
#            ),
        ]
    ),
    color="#4D3227",
    dark=True,
    id='navbar',
    )
    return navbar

# Create footer section
def createFooter():
    return html.Footer([html.Span("Footer section")], className='footer')

# Create two columns of videos with given 'rows'
def createVidColumns(youtubeAPI, rows):
    return html.Div(children=[
         html.Div(className='video-list-column', 
                  children=[createVidButton(i, youtubeAPI.getThumbnail(i)) for i in range(rows)]),
         html.Div(className='video-list-column', 
                  children=[createVidButton(i, youtubeAPI.getThumbnail(i)) for i in range(rows, 2 * rows)]),
    ], style={'textAlign':'center', 'background-color':'#EBC999'})

# Helper function to create a clickable image anchor
def createVidButton(index, imgUrl):
    anchorId = 'anchor-' + str(index+1)
    return html.Div(className='video-list-item', children=[
        html.A(className='video-anchor', id=anchorId, children=[
            html.Img(className='video-thumbnail', src=imgUrl),
            html.Img(className="video-play", src='/assets/images/play.png')
        ])
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