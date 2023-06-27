import models

import pymongo
import datetime
import time

def strToMs(text_time: str) -> int:
    arr = text_time.split(':')
    time_s = 0
    for i in range(len(arr)):
        timeInt = int(arr[-abs(i)-1])
        if i == 0:
            time_s += timeInt
        elif i == 1:
            time_s += timeInt * 60
        elif i == 2:
            time_s += timeInt * 60 * 60
    return time_s



class Controller:
    def __init__(self, mongo_client: pymongo.MongoClient):
        self.client = mongo_client


class VideolangController(Controller):
    def __init__(self, mongo_client):
        super().__init__(mongo_client)
        self.videolang_db = self.client.get_database('videolang')

        self.__connect_collections()

    def get_new_videos(self, channel_name):
        channel = models.Channel(channel_name)
        channel.get()
        pack_iter = channel.iter_all_videos()
        video_dont_exist = True
        new_videos = []
        while video_dont_exist:
            try:
                pack = next(pack_iter)
                if pack == None:
                    break
            except:
                break
            for video in pack:
                video_in_db = self.videos_collection.find_one({"video_id": video['content']['videoRenderer']['videoId']})
                if video_in_db == None:
                    self.videos_collection.insert_one(self.__parse_video(channel_name, video))
                    new_videos.append(self.__parse_video(channel_name, video))
                else:
                    video_dont_exist = False
                    break
        return new_videos

    def fast_get_channel_videos(self, channel_name) -> list:
        old_videos = list(self.videos_collection.find({'author': channel_name}))
        if len(old_videos) == 0:
            return self.get_channel_videos(channel_name)
        new_videos = self.get_new_videos(channel_name)
        return new_videos + old_videos

    def get_uptodate_channel_videos(self, channel_name) -> list:
        """
            Gets all videos from the channel (going though full channel, so takes more time)
        """
        self.update_channel_videos(channel_name)
        return list(self.videos_collection.find({'author': channel_name}))
    
    def update_channel_videos(self, channel_name):
        channel = models.Channel(channel_name)
        channel.get()
        raw_videos = channel.get_all_videos()
        for raw_video in raw_videos:
            video = self.__parse_video(channel_name, raw_video)
            self.videos_collection.find_one_and_update({'video_id': video['video_id']}, {'$set': video}, upsert=True)

    
    def __parse_video(self, channel_name, video):
        video_renderer = video['content']['videoRenderer']
        video_id = video_renderer['videoId']
        title = video_renderer['title']['runs'][0]['text']
        thumbnails = video_renderer['thumbnail']
        try:
            description = video_renderer['descriptionSnippet']['runs'][0]['text']
        except:
            description = ""
        text_time = video_renderer['lengthText']['simpleText']
        duration = strToMs(text_time) * 1000

        data = {
            "video_id": video_id,
            "author": channel_name,
            "title": title,
            "thumbnail": thumbnails,
            "description": description,
            "durationMs": duration,
            "viewsCount": 0,
            "category_vector": {
                "category": None,
                "level": 0
            },
            "hidden": False
        }
        return data

    def __connect_collections(self): 
        # may be error?
        try:
            self.videos_collection = self.videolang_db.create_collection('videos2')
            self.transcriptions_collection = self.videolang_db.create_collection('transcriptions')
            self.authors_collection = self.videolang_db.create_collection('authors')
            self.deprecated_videos_collection = self.videolang_db.create_collection('deprecated_videos')
        except:
            self.videos_collection = self.videolang_db.get_collection('videos2')
            self.transcriptions_collection = self.videolang_db.get_collection('transcriptions')
            self.authors_collection = self.videolang_db.get_collection('authors')
            self.deprecated_videos_collection = self.videolang_db.get_collection('deprecated_videos')