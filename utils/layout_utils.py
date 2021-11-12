import dash_html_components as html

def getVidIframe(url):
    return html.Iframe(src=url,
                       width="420",
                       height="255"
    )