from apiclient.discovery import build

# YoutubeAPI wrapper
class YoutubeAPI:

    def __init__(self, api_key):
        self.youtubeAPI = build('youtube', 'v3', developerKey = api_key)
        self.currentIndex = 0
        self.query = "cute animals"

    # check values are the values of the toggled on animal checkboxes
    def setQuery(self, checkedValues):
        query = ""
        if len(checkedValues) > 0:
            for value in checkedValues:
                query = query + " | " + "cute" + value;
        else:
            query = "cute animals"
        self.query = query;
        
    # query for videos
    def search(self, resultsPerPage):
        request = self.youtubeAPI.search().list(q=self.query, part='snippet', type='video', videoEmbeddable='true', maxResults=resultsPerPage)
        response = request.execute()
        self.videoIds = []
        for item in response['items']:
            self.videoIds.append(item['id']['videoId'])
        self.populateList()
        
    # Use fake search data to get around API call limit
    def fake_search(self, resultsPerPage):
        self.videoIds = []
        groupSize = (int)(resultsPerPage / 6)
        for i in range(groupSize):
            self.videoIds.append('C9OMAX91oyw')
            self.videoIds.append('2GEv876ZRI0')
            self.videoIds.append('aPzipib6n7g')
            self.videoIds.append('oY8Jq0pyYtA')
            self.videoIds.append('5RystI_zIow')
            self.videoIds.append('RQkWvoES_uQ')
        
        self.populateList()
    
    def populateList(self):
        self.urls = []
        self.thumbnails = []
        
        for videoId in self.videoIds:
            url = 'https://www.youtube.com/embed/' + videoId + '?autoplay=1'
            thumbnail = 'https://i.ytimg.com/vi/' + videoId + '/mqdefault.jpg'
            self.urls.append(url)
            self.thumbnails.append(thumbnail)
    
            
    # Set current / select video    
    def setCurrentVid(self, index):
        self.currentIndex = index
        
    # Get thumbnail's URL
    def getThumbnail(self, index):
        return self.thumbnails[index]
    
    # Get embeded video's url
    def getCurrentUrl(self):
        return self.urls[self.currentIndex]
        
        
        
    

# Determine search keywords
def getVidSearchKeywords(button_id):
    if button_id == "puppy-button":
        return "cute puppies"
    elif button_id == "kitten-button":
        return "cute kittens"
    else:
        return "cute animals"