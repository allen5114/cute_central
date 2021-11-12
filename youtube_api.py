
# Determine search keywords
def getVidSearchKeywords(button_id):
    if button_id == "puppy-button":
        return "cute puppies"
    elif button_id == "kitten-button":
        return "cute kittens"
    else:
        return "cute animals"

# Search for videos using Youtube API..to do
def searchVids(searchKeywords):
    urls = []
    urls = ['https://www.youtube.com/embed/wtb1e6MYEek' for i in range(10)]
    return urls