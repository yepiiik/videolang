import grequests
import requests
import re
import time
import json
import pymongo

from fake_useragent import UserAgent


class Guide_Builder:
    def __init__(self):
        self.html = ''
        self.json_data = None

        self.get()
        self.__get_guide_builder_data()


    def get(self):
        url = "https://www.youtube.com/feed/guide_builder"
        header = {
            "user-agent": ua.random
        }
        conn = requests.get(url, headers=header)
        self.html = conn.text
        conn.close()


    def __get_guide_builder_data(self):
        scripts = re.findall('<script[^>]*>(.*?)<\/script>', self.html)
        # searching for all <script> in html response
        for script in scripts:
            # is <script> block contain string starts with (webCommandMetadata) and ends with (guide_builder)
            if re.search('webCommandMetadata.+guide_builder', script):
                self.json_data = json.loads(re.findall('{.+}', script)[0])

ua = UserAgent()


if __name__ == "__main__":
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["videolang"]

    print(mydb.list_collection_names())


    guide_builder = Guide_Builder()
    json_data = guide_builder.json_data
    sectionListRenderer = json_data['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents']
    for itemSectionRenderer in sectionListRenderer:
        print(itemSectionRenderer['itemSectionRenderer']['contents'][0]['shelfRenderer']['title']['runs'])
        horizontalListRenderer = itemSectionRenderer['itemSectionRenderer']['contents'][0]['shelfRenderer']['content']['horizontalListRenderer']['items']
        for gridChannelRenderer in horizontalListRenderer:
            print(gridChannelRenderer['gridChannelRenderer']['title'])

