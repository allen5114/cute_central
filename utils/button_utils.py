import dash

# Get the ID of the last clicked element
def getClickedElementID():
    ctx = dash.callback_context
    if not ctx.triggered:
        return None
    else:
        return ctx.triggered[0]['prop_id'].split('.')[0]
