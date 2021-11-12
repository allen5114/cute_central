from apiclient.discovery import build

# YoutubeAPI wrapper
class YoutubeAPI:

    def __init__(self, api_key):
        self.youtubeAPI = build('youtube', 'v3', developerKey = api_key)
        
    # query for videos
    def search(self, keywords):
        request = self.youtubeAPI.search().list(q=keywords, part='snippet', type='video', maxResults=20)
        response = request.execute()
        urls = []
        for item in response['items']:
            print(item['id']['videoId'])
            url = 'https://www.youtube.com/embed/' + item['id']['videoId']
            urls.append(url)
        return urls

# Determine search keywords
def getVidSearchKeywords(button_id):
    if button_id == "puppy-button":
        return "cute puppies"
    elif button_id == "kitten-button":
        return "cute kittens"
    else:
        return "cute animals"