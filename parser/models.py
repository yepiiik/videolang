import grequests
import requests
import re
import json

from fake_useragent import UserAgent


class Guide_Builder():
    def __init__(self):
        self.url = "https://www.youtube.com/feed/guide_builder"
        self.response = None
        self.json_data = None
        self.formated_data = dict()
        self.ua = UserAgent()
        self.header = {
            "accept-language": "en-US,en;q=0.9",
            "user-agent": self.ua.random
        }

    def get(self):
        conn = requests.get(self.url, headers=self.header)
        self.html = conn.text
        conn.close()

        # parse html and then update self.json_data
        self.__get_guide_builder_data()
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
                print(channel_name)
                channel_list.append(channel_name)
            self.formated_data[title] = channel_list
