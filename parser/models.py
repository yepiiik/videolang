import grequests
import requests
import re
import json

from fake_useragent import UserAgent


ua = UserAgent()

def search_within_scripts(regex, html):
    # getting all script in html
    scripts = re.findall('<script[^>]*>(.*?)<\/script>', html)
    for script in scripts:
        # searching for script that contain essential json data
        if re.search(regex, script):
            clear_json = re.findall('{.+}', script)[0]
            return json.loads(clear_json)


class Watch:
    def __init__(self):
        self.video_id = ''
        self.header = {
            "accept-language": "en-US,en;q=0.9",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19577"
        }
        self.params = dict()
        self.json_data = None
        self.transcription = None

    def get(self, id):
        self.video_id = id
        print(self.header["user-agent"])
        conn = requests.get(f"https://www.youtube.com/watch?v={id}", headers=self.header)
        self.html = conn.text
        conn.close()
        self.json_data = search_within_scripts("getTranscriptEndpoint", self.html)
        self.__parse_json()

    def get_transcription(self):
        with open("parser/get_transcription.json", "r") as file:
            data = json.load(file)
            data["params"] = self.json_data["engagementPanels"][-1]["engagementPanelSectionListRenderer"]["content"]["continuationItemRenderer"]["continuationEndpoint"]["getTranscriptEndpoint"]["params"]
        conn = requests.post("https://www.youtube.com/youtubei/v1/get_transcript?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8&prettyPrint=false", headers=self.header, data=json.dumps(data))
        self.transcription = conn.text
        conn.close()

    def __get_data(self):
        # getting all script in html
        scripts = re.findall('<script[^>]*>(.*?)<\/script>', self.html)
        for script in scripts:
            # searching for script that contain essential json data
            if re.search('getTranscriptEndpoint', script):
                clear_json = re.findall('{.+}', script)[0]
                self.json_data = json.loads(clear_json)



class Channel():
    """
        Creating channel model to get information from differant channels
    """
    def __init__(self, channel_name=None):
        self.html = None
        self.formated_data = dict()
        self.header = {
            "accept-language": "en-US,en;q=0.9",
            "user-agent": ua.random
        }
        self.json_data = None
        self.video_ids = []
        self.videos = []
        self.channel_name = channel_name
        self._continuationItem = None
        self._continuationToken = None

    def get(self):
        """
            Enter channel name for example: mrbeast
        """
        
        conn = requests.get(f"https://www.youtube.com/@{self.channel_name}", headers=self.header)
        self.html = conn.text
        conn.close()

        self.json_data = search_within_scripts("videosCountText", self.html)
        try:
            self.__channel_parse_json()
        except TypeError:
            pass

    def get_all_videos(self):
        self.get_videos_pack()
        while True:
            print(len(self.video_ids))
            try:
                self.browse()
            except BaseException:
                break
        print(len(self.video_ids))

    def get_videos_pack(self):
        conn = requests.get(f"https://www.youtube.com/@{self.channel_name}/videos", headers=self.header)
        self.html = conn.text
        conn.close()

        self.json_data = search_within_scripts("browseEndpoint", self.html)
        try:
            self.__videos_pack_parse_json()
        except:
            pass

    def browse(self):      
        with open("parser/get_videos_content2.json", "r") as file:
            data = json.load(file)
            if self._continuationToken != None:
                data["continuation"] = self._continuationToken

        conn = requests.post("https://www.youtube.com/youtubei/v1/browse?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8&prettyPrint=false", headers=self.header, data=json.dumps(data))
        self.json_data = conn.json()
        conn.close()

        self.__browse_parse_json()

    def __get_json_from_html_scripts(self, keyword, html):
        # getting all script in html
        scripts = re.findall('<script[^>]*>(.*?)<\/script>', html)
        for script in scripts:
            # searching for script that contain essential json data
            if re.search(keyword, script):
                clear_json = re.findall('{.+}', script)[0]
                self.json_data = json.loads(clear_json)

    def __channel_parse_json(self):
        json_data = self.json_data
        videosCountText = json_data["header"]["c4TabbedHeaderRenderer"]["videosCountText"]["runs"][0]["text"]
        try:
            self.videosCount = int(videosCountText)
        except ValueError:
            self.videosCount = 0

    def __browse_parse_json(self):
        json_data = self.json_data
        contents = json_data["onResponseReceivedActions"][0]["appendContinuationItemsAction"]["continuationItems"]
        self.__videos_parse_json(contents)


    def __videos_pack_parse_json(self):
        self.formated_data.clear()
        json_data = self.json_data
        category = json_data["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][1]["tabRenderer"]
        if category["title"] == "Videos":
            contents = category["content"]["richGridRenderer"]["contents"]
            self.__videos_parse_json(contents)

    def __videos_parse_json(self, contents):
        for content in contents:
            if "richItemRenderer" in content:
                self.videos.append(content["richItemRenderer"])
                self.video_ids.append(content["richItemRenderer"]["content"]["videoRenderer"]["videoId"])
            elif "continuationItemRenderer" in content:
                self._continuationItem = content
                self._continuationToken = content["continuationItemRenderer"]["continuationEndpoint"]["continuationCommand"]["token"]
                continuationTokenExist = True
        if continuationTokenExist != True:
            raise(BaseException())


class Guide_Builder():
    def __init__(self):
        self.url = "https://www.youtube.com/feed/guide_builder"
        self.response = None
        self.json_data = None
        self.formated_data = []
        self.header = {
            "accept-language": "en-US,en;q=0.9",
            "user-agent": ua.random
        }

    def get(self):
        conn = requests.get(self.url, headers=self.header)
        self.html = conn.text
        conn.close()

        # parse html and then update self.json_data
        self.json_data = search_within_scripts("webCommandMetadata.+guide_builder", self.html)
        self.__parse_json()

    def __get_guide_builder_data(self):
        # getting all script in html
        scripts = re.findall('<script[^>]*>(.*?)<\/script>', self.html)
        for script in scripts:
            # searching for script that contain essential json data
            if re.search('webCommandMetadata.+guide_builder', script):
                clear_json = re.findall('{.+}', script)[0]
                self.json_data = json.loads(clear_json)

    def __parse_json(self):
        self.formated_data.clear()
        json_data = self.json_data
        sectionListRenderer = json_data['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents']
        for itemSectionRenderer in sectionListRenderer:
            title = itemSectionRenderer['itemSectionRenderer']['contents'][0]['shelfRenderer']['title']['runs'][0]['text']
            channel_list = []
            horizontalListRenderer = itemSectionRenderer['itemSectionRenderer']['contents'][0]['shelfRenderer']['content']['horizontalListRenderer']['items']
            for gridChannelRenderer in horizontalListRenderer:
                channel_name = gridChannelRenderer['gridChannelRenderer']['title']['simpleText']
                channel_link = gridChannelRenderer["gridChannelRenderer"]["navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"]
                channel_list.append({"username": channel_name, "link": channel_link})
            category = {
                "title": title,
                "channels": channel_list
            }
            self.formated_data.append(category)


