import grequests
import requests
import re
import json
import time

from fake_useragent import UserAgent


ua = UserAgent()

       
class Base:
    @staticmethod
    def search_within_scripts(regex, scripts) -> dict | None:
        for script in scripts:
            # searching for script that contain essential json data
            if re.search(regex, script):
                clear_json = re.findall('{.+}', script)[0]
                return json.loads(clear_json)
    
    @staticmethod
    def get_scripts(html):
        return re.findall('<script[^>]*>(.*?)<\/script>', html)


class Watch(Base):
    def __init__(self, video_id, session):
        self.video_id = video_id
        self.header = {
            # "authority": "www.youtube.com",
            # "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            # "sec-fetch-dest": "document",
            # "sec-fetch-mode": "navigate",
            # "sec-fetch-site": "none",
            # "sec-fetch-user": "?1",
            # "service-worker-navigation-preload": "true",
            # "upgrade-insecure-requests": "1",
            "accept-language": "en-US,en;q=0.5",
            "accept-charset": "utf-8",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19577"
        }
        self.params = dict()
        self.json_data = None
        self.transcription = None

        self.session: grequests.Session = session

    def get(self):
        print(f"Get video info for: https://youtube.com/watch?v={self.video_id}")
        conn = self.session.get(f"https://www.youtube.com/watch?v={self.video_id}", headers=self.header)
        self.html = conn.text
        conn.close()
        self.scripts = self.get_scripts(self.html)
        return self.html
        # self.__parse_json()

    def get_async_request(self) -> grequests.AsyncRequest:
        async_request = grequests.get(f"https://www.youtube.com/watch?v={self.video_id}", headers=self.header, session=self.session)
        return async_request
    
    def get_video(self):
        self.get()
        short_info = self.search_within_scripts('author', self.scripts)['videoDetails']
        microformat = self.search_within_scripts('playerMicroformatRenderer', self.scripts)['microformat']['playerMicroformatRenderer']

        return microformat

    def get_transcription(self) -> dict | None:
        self.get()
        self.json_data = super().search_within_scripts("getTranscriptEndpoint", self.scripts)
        if self.get() == None:
            return
        with open("get_transcription.json", "r") as file:
            data = json.load(file)
            data['context']['client']['originalUrl'] = "https://youtube/watch?v=" + self.video_id
            data["params"] = self.json_data["engagementPanels"][-1]["engagementPanelSectionListRenderer"]["content"]["continuationItemRenderer"]["continuationEndpoint"]["getTranscriptEndpoint"]["params"]
        conn = self.session.post("https://www.youtube.com/youtubei/v1/get_transcript?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8&prettyPrint=false", headers=self.header, data=json.dumps(data))
        self.transcription = json.loads(conn.text)['actions'][0]['updateEngagementPanelAction']['content']['transcriptRenderer']
        conn.close()
        return self.transcription
    
    def get_transcription_async_request(self) -> grequests.AsyncRequest:
        with open("get_transcription.json", "r") as file:
            data = json.load(file)
            try:
                data['context']['client']['originalUrl'] = "https://youtube/watch?v=" + self.video_id
                data["params"] = self.json_data["engagementPanels"][-1]["engagementPanelSectionListRenderer"]["content"]["continuationItemRenderer"]["continuationEndpoint"]["getTranscriptEndpoint"]["params"]
            except:
                print("ERROR: get_transcripton_async_request")
                return
        async_request = grequests.post("https://www.youtube.com/youtubei/v1/get_transcript?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8&prettyPrint=false", headers=self.header, data=json.dumps(data), session=self.session)
        return async_request

    def __get_data(self):
        # getting all script in html
        scripts = re.findall('<script[^>]*>(.*?)<\/script>', self.html)
        for script in scripts:
            # searching for script that contain essential json data
            if re.search('getTranscriptEndpoint', script):
                clear_json = re.findall('{.+}', script)[0]
                self.json_data = json.loads(clear_json)


class Channel(Base):
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
        self.session = requests.session()

    def post_consent(self):
        with open("consent.json", "r") as file:
            data = json.load(file)

        conn = self.session.post(f"https://consent.youtube.com/save", headers=self.header, data=data)
        self.cookies = conn.cookies
        print(conn.status_code)
        conn.close()

    def get(self) -> str:
        """
            The output is raw HTML
        """
        self.post_consent()
        conn = self.session.get(f"https://www.youtube.com/@{self.channel_name}", headers=self.header)
        self.html = conn.text
        conn.close()

        self.scripts = self.get_scripts(self.html)
        self.json_data = super().search_within_scripts("videosCountText", self.scripts)
        try:
            self.__channel_parse_json()
        except TypeError:
            pass
        
        return self.html

    def get_all_videos(self) -> list:
        hasStartPoint = False # Variable to evaluate whether first query was executed
        
        while True:
            print(self._continuationToken)
            try:
                if not hasStartPoint:
                    self.get_videos_pack()
                self.browse()
            except BaseException:
                break
        print(len(self.video_ids))
        return self.videos

    def iter_all_videos(self):
        hasStartPoint = False # Variable to evaluate whether first query was executed

        while True:
            print(self._continuationToken)
            try:
                if not hasStartPoint:
                    yield self.get_videos_pack()
                yield self.browse()
            except BaseException:
                break
        print(len(self.video_ids))
        return None

    def get_videos_pack(self):
        conn = self.session.get(f"https://www.youtube.com/@{self.channel_name}/videos", headers=self.header)
        self.html = conn.text
        conn.close()

        self.scripts = self.get_scripts(self.html)
        start = time.time()

        self.json_data = super().search_within_scripts("browseEndpoint", self.scripts)
        with open(f"api/data/{self.channel_name}.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(self.json_data))

        result = self.__videos_pack_parse_json()
        total = time.time() - start
        print(total)
        return result


    def browse(self, continuationToken=None):
        with open("api/get_videos_content2.json", "r") as file:
            data = json.load(file)
            if self._continuationToken != None:
                data["continuation"] = self._continuationToken
            elif continuationToken != None:
                data["continuation"] = continuationToken

        conn = self.session.post("https://www.youtube.com/youtubei/v1/browse?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8&prettyPrint=false", headers=self.header, data=json.dumps(data), cookies=self.cookies)
        self.json_data = conn.json()
        conn.close()
        return self.__browse_parse_json() # videos pack

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
        pack = self.__videos_parse_json(contents)
        return pack # videos pack


    def __videos_pack_parse_json(self):
        self.formated_data.clear()
        json_data = self.json_data
        category = json_data["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][1]["tabRenderer"]
        if category["title"] == "Videos":
            contents = category["content"]["richGridRenderer"]["contents"]
            return self.__videos_parse_json(contents)

    def __videos_parse_json(self, contents):
        pack = []
        continuationTokenExist = False
        for content in contents:
            print(content)
            if "richItemRenderer" in content:
                self.videos.append(content["richItemRenderer"]) # add video to videos array (there may be memory leaks)
                pack.append(content["richItemRenderer"]) # add video to local pack (there may be memory leaks)
                self.video_ids.append(content["richItemRenderer"]["content"]["videoRenderer"]["videoId"])
            elif "continuationItemRenderer" in content:
                self._continuationItem = content
                self._continuationToken = content["continuationItemRenderer"]["continuationEndpoint"]["continuationCommand"]["token"]
                continuationTokenExist = True
        if continuationTokenExist != True:
            raise(BaseException())
        return pack


class Guide_Builder(Base):
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
        self.scripts = self.get_scripts(self.html)
        self.json_data = super().search_within_scripts("webCommandMetadata.+guide_builder", self.scripts)
        return self.__parse_json()

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
        return self.formated_data


