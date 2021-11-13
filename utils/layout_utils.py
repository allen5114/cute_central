#import dash_html_components as html

import dash_bootstrap_components as dbc
from dash import Input, Output, State, html


# Utils function to put Youtube video in iframe
def getVidIframe(url):
    return html.Iframe(src=url,
                       width="420",
                       height="255"
    )