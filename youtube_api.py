from apiclient.discovery import build

# YoutubeAPI wrapper
class YoutubeAPI:

    def __init__(self, api_key):
        self.youtubeAPI = build('youtube', 'v3', developerKey = api_key)
        self.currentIndex = 0
        self.query = "cute animals"
        self.order = 'relevance'
        self.urls = []
        self.thumbnails = []

    # check values are the values of the toggled on animal checkboxes
    def setQuery(self, checkedValues):
        query = ""
        if len(checkedValues) > 0:
            for value in checkedValues:
                query = query + " | " + "cute" + value + " compilation";
        else:
            query = "cute animals compilation"
        self.query = query
    
    # set sort order used when querying
    def setOrder(self, order):
        self.order = order
        
    # query for videos
    def search(self, resultsPerPage):
        request = self.youtubeAPI.search().list(q=self.query, order=self.order, part='snippet', type='video', videoEmbeddable='true', maxResults=resultsPerPage)
        try:
            response = request.execute()
            self.videoIds = []
            for item in response['items']:
                self.videoIds.append(item['id']['videoId'])
            self.populateList()
        except:
            self.videoIds = []
            print("Failed to query the videos. Please check the Youtube API key");
        
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
            url = 'https://www.youtube.com/embed/' + videoId + '?autoplay=1&playsinline=0"'
            thumbnail = 'https://i.ytimg.com/vi/' + videoId + '/mqdefault.jpg'
            self.urls.append(url)
            self.thumbnails.append(thumbnail)
    
            
    # Set current / select video    
    def setCurrentVid(self, index):
        self.currentIndex = index
        
    # Get thumbnail's URL
    def getThumbnail(self, index):
        if len(self.thumbnails) > index:
            return self.thumbnails[index]
        return None;
    
    # Get embeded video's url
    def getCurrentUrl(self):
        if len(self.urls) > self.currentIndex:
            return self.urls[self.currentIndex]
        return None;
    
    # Get number of results
    def getResultCount(self):
        return len(self.videoIds)
        
        
        
    

# Determine search keywords
def getVidSearchKeywords(button_id):
    if button_id == "puppy-button":
        return "cute puppies"
    elif button_id == "kitten-button":
        return "cute kittens"
    else:
        return "cute animals"