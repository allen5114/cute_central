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
            children=[
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src='/assets/images/icon.png', height="30px"),),
                            dbc.Col(dbc.NavbarBrand("Cute Central", className="logo-text")),
                        ],
                        align="center",
                        className="g-0",
                    ),
                    style={"textDecoration": "none"},
                ),
                createSearchButton(),
            ],
        ),
        color="#4D3227",
        id='navbar',

    )

def createTermsOfUse():
    modalHeader = dbc.ModalHeader("")
    modalChildren = [html.H3("Terms of Use"),
                     html.Span("Your access to and use of the Service is conditioned on your acceptance of and compliance with these terms. These Terms apply to all visitors, users, and others who access or use the Service."),
                     html.Br(), html.Br(),
                     html.H5("Youtube's Terms of Service"),
                     html.Span("Youtube API Clients is used to provide the content. By using this site, you are agreeing to be bound by the "),
                     html.A("Youtube Terms of service",
                            href="https://www.youtube.com/t/terms", 
                            target="_blank")]
    return getModal('terms-modal', 'terms-body', False, modalHeader, modalChildren, None)

def createPrivacyPolicy():
    modalHeader = dbc.ModalHeader("")
    modalChildren = [html.H3("Privacy Policy"),
                     html.Span("Youtube API is used to provide content and it's provided in accordance with "),
                     html.A("Google Privacy Policy", href="http://www.google.com/policies/privacy", target="_blank"),
                     html.Br(), html.Br(),
                     html.Span("Google and or third-party service providers are used for advertisements, promotions, and offers. Third-party vendors, including Google, use cookies to serve ads based on user’s prior visits on this site. Google’s use of advertising cookies enables it and its partner to serve ads to you based on your visits to our site. You may opt-out of personalized advertisement through browser setting or visiting "),
                     html.A("Ads Settings", href="https://www.google.com/settings/ads", target="_blank"),
                     ]
    return getModal('privacy-policy-modal', 'privacy-policy-body', False, modalHeader, modalChildren, None)

# Create footer section
def createFooter():
    return html.Footer(children=[createTermsOfUse(),
                                 createPrivacyPolicy(),
                                 html.A("Terms of Use", className="footer-link", id="terms_of_use_button"),
                                 html.Br(),
                                 html.A("Privacy Policy", className="footer-link", id="privacy-policy-button"),
                                 html.Br(),
                                 html.A("Contact Developer", className="footer-link", href="mailto:chuan.l.hung@gmail.com")],
                        className='footer', id='footer')

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
        persistence=True,
        id="sortby-options"
    )], style={'textAlign':'center'})


# Create a modal that embeds a video
def createVideoModal(youtubeAPI):
    modalHeader = dbc.ModalHeader("")
    modalChildren = [html.Iframe(id="iframe-player", 
                                 src=youtubeAPI.getCurrentUrl(),
                                 allow="autoplay; fullscreen;")]
                                 #sandbox="allow-same-origin",
                                 #referrerPolicy="origin-when-cross-origin")]
    return getModal('modal-fs', 'player', True, modalHeader, modalChildren, None)

# Create a modal that allows the user to modify search query
def createSearchFilterModel(youtubeAPI):
    modalHeader = dbc.ModalHeader("")
    modalChildren = [html.H5("Search Options"),
                     getSortOptions(),
                     html.Br(),
#                     html.Hr(),
                     html.H5("Your weaknesses"),
                     dcc.Dropdown(id='search-checklist',
                                   multi=True,
                                   persistence=True,
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
    