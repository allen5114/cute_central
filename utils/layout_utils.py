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
    return html.Footer([html.Span("Footer section")], className='footer', id='footer')

# Create list of videos
def createVideos(youtubeAPI, rows, columns):
    return html.Div(id="videos", children=[createVidColumns(youtubeAPI, rows, columns)])

# Create columns of videos with given 'rows'
def createVidColumns(youtubeAPI, rows, columns):
    vids = []
    for column in range(columns):
        group = []
        for row in range(rows):
            index = column * rows + row
            idDict = {'type': 'video-anchor', 'index': index}
            group.append(getVideoAnchor(idDict, youtubeAPI.getThumbnail(index)))
        vids.append(html.Div(className='video-list-column', children=group))
    return html.Div(children=vids)

# Sortby options
def getSortOptions():
    return html.Div([dcc.Dropdown(
        options=[{'label': 'Relevance', 'value': 'relevance'},
                 {'label': 'Rating', 'value': 'rating'},
                 {'label': 'View Count', 'value': 'viewCount'},
                 {'label': 'Upload Date', 'value': 'date'}],
        value='relevance',
        id="sortby-options"
    )], style={'textAlign':'center'})


# Create a modal that embeds a video
def createVideoModal(youtubeAPI):
    modalHeader = dbc.ModalHeader("")
    modalChildren = [html.Iframe(src=youtubeAPI.getCurrentUrl(), width="90%", height="90%", allow="autoplay")]
    return getModal('modal-fs', 'player', True, modalHeader, modalChildren, None)

# Create a modal that allows the user to modify search query
def createSearchFilterModel(youtubeAPI):
    modalHeader = dbc.ModalHeader("")
    modalChildren = [html.H5("Search Options"),
                     getSortOptions(),
                     html.Br(),
                     html.Hr(),
                     html.H5("Your weaknesses"),
                     dcc.Dropdown(id='search-checklist',
                                   multi=True,
                                   options=[{'label': 'Infants / Toddlers', 'value': 'infants toddlers'},
                                            {'label': 'Puppies', 'value': 'puppies'},
                                            {'label': 'Kittens', 'value': 'kittens'},
                                            {'label': 'Pandas', 'value': 'baby pandas'},
                                            {'label': 'Rabbits', 'value': 'baby rabbits'},
                                            {'label': 'Penguins', 'value': 'baby penguins'},
                                            {'label': 'Hedgehogs', 'value': 'baby hedgehogs'},
                                            {'label': 'Sea Otters', 'value': 'baby sea otters'},
                                            {'label': 'Quokkas', 'value': 'quokkas'}],
                                   value=['infants toddlers', 'puppies', 'kittens'])]
    modalFooter = dbc.ModalFooter(dbc.Button("Search", id='search-topics-button', n_clicks=0))
    return getModal('search-filter-modal', 'filter-body', False, modalHeader, modalChildren, modalFooter)
    