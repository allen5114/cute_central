import dash

# Get the ID of the last clicked category button
def getClickedButtonID():
    ctx = dash.callback_context
    if not ctx.triggered:
        return None
    else:
        return ctx.triggered[0]['prop_id'].split('.')[0]