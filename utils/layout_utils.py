import dash_bootstrap_components as dbc

from dash import html, dcc
from utils.component_factory import getImageAnchor, getVideoAnchor, getModal

# Helper function to create a clickable image anchor
def createSearchButton():
    return html.Div(children=[getImageAnchor('search_button', 'search-icon', '/assets/images/search.png')])

# Create navigation bar
def createNavBar():
    return dbc.Navbar(
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
                createSearchButton(),
            ]
        ),
        color="#4D3227",
        dark=True,
        id='navbar',
    )

# Create footer section
def createFooter():
    return html.Footer([html.Span("Footer section")], className='footer')

# Create list of videos
def createVideos(youtubeAPI, rows):
    return html.Div(id="videos", children=[createVidColumns(youtubeAPI, rows)])


# Create two columns of videos with given 'rows'
def createVidColumns(youtubeAPI, rows):
    return html.Div(children=[
         html.Div(className='video-list-column', 
                  children=[getVideoAnchor('anchor-' + str(i+1), youtubeAPI.getThumbnail(i)) for i in range(rows)]),
         html.Div(className='video-list-column', 
                  children=[getVideoAnchor('anchor-' + str(i+1), youtubeAPI.getThumbnail(i)) for i in range(rows, 2 * rows)]),
    ])

# Create a modal that embeds a video
def createVideoModal(youtubeAPI):
    modalChildren = [html.Iframe(src=youtubeAPI.getCurrentUrl(), width="90%", height="90%", allow="autoplay")]
    return getModal('modal-fs', 'player', True, modalChildren)

# Create a modal that allows the user to modify search query
def createSearchFilterModel(youtubeAPI):
    modalChildren = [dcc.Checklist(id='search-checklist',
                                   options=[{'label': 'Puppies', 'value': 'puppies'},
                                            {'label': 'Kittens', 'value': 'kittens'}],
                                   value=['puppies']),
                     html.Br(),
                     dbc.Button("Search", id='search-topics-button', n_clicks=0)]
    return getModal('search-filter-modal', 'filter-body', False, modalChildren)
    