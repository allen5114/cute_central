from apiclient.discovery import build

# YoutubeAPI wrapper
class YoutubeAPI:

    def __init__(self, api_key):
        self.youtubeAPI = build('youtube', 'v3', developerKey = api_key)
        self.currentIndex = 0
        
    # query for videos
    def search(self, keywords):
        request = self.youtubeAPI.search().list(q=keywords, part='snippet', type='video', videoEmbeddable='true', maxResults=6)
        response = request.execute()
        urls = []
        self.videoIds = []
        for item in response['items']:
            #print(item['id']['videoId'])
            url = 'https://www.youtube.com/embed/' + item['id']['videoId']
            urls.append(url)
            self.videoIds.append(item['id']['videoId'])
        self.populateList()
        return urls
        
    # query for videos
    def search2(self, keywords):
        request = self.youtubeAPI.search().list(q=keywords, part='snippet', type='video', videoEmbeddable='true', maxResults=6)
        response = request.execute()
        urls = []
        thumbnails = []
        #print(response)
        for item in response['items']:
            #print(item['id']['videoId'])
            url = 'https://www.youtube.com/embed/' + item['id']['videoId']
            urls.append(url)
            thumbnails.append(item['snippet']['thumbnails']['medium']['url'])
        return urls, thumbnails
        
    # Use fake search data to get around API call limit
    def fake_search(self):
        self.videoIds = []
        self.urls = []
        self.thumbnails = []
        
        self.videoIds.append('C9OMAX91oyw')
        self.videoIds.append('2GEv876ZRI0')
        self.videoIds.append('aPzipib6n7g')
        self.videoIds.append('oY8Jq0pyYtA')
        self.videoIds.append('5RystI_zIow')
        self.videoIds.append('RQkWvoES_uQ')
        
        for videoId in self.videoIds:
            url = 'https://www.youtube.com/embed/' + videoId + '?autoplay=1'
            thumbnail = 'https://i.ytimg.com/vi/' + videoId + '/mqdefault.jpg'
            self.urls.append(url)
            self.thumbnails.append(thumbnail)
    
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