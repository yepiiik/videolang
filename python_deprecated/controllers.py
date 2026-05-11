import models

import grequests
import pymongo
import datetime
import time
import json
import re

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
        self.video_document_example = {
            "video_id": '',
            "username": '',
            "channel_id": '',
            "title": '',
            "thumbnail": [],
            "description": '',
            "durationMs": 0,
            "viewsCount": 0,
            "publishDate": datetime.datetime(1970, 1, 1),
            "uploadDate": datetime.datetime(1970, 1, 1),
            "category_vector": {},
            "hidden": False
        }
        self.category_document_example = {
            'username': '',
            'link': '',
            'category': ''
        }

        self.__connect_collections()

    def get_categories(self):
        pass

    def update_categories(self):
        guide_builder = models.Guide_Builder()
        categories = guide_builder.get()

        for category in categories:
            for channel in category['channels']:
                document = {
                    'username': channel['username'],
                    'link': channel['link'],
                    'category': category['title']
                }
                self.categories_collaction.update_one({'link': channel['link']}, {'$set': document}, upsert=True)

    def get_new_videos(self, channel_name):
        channel = models.Channel(channel_name)
        channel.get()
        self.session = channel.session
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

    def get_channel_videos(self, channel_name) -> list:
        old_videos = list(self.videos_collection.find({'username': channel_name}))
        if len(old_videos) == 0:
            return self.get_uptodate_channel_videos(channel_name)
        new_videos = self.get_new_videos(channel_name)
        return new_videos + old_videos

    def get_uptodate_channel_videos(self, channel_name) -> list:
        """
            Gets all videos from the channel (going though full channel, so takes more time)
        """
        self.update_channel_videos(channel_name)
        return list(self.videos_collection.find({'username': channel_name}))
    
    def update_channel_videos(self, channel_name):
        channel = models.Channel(channel_name)
        channel.get()
        self.session = channel.session
        raw_videos = channel.get_all_videos()
        print(raw_videos)
        for raw_video in raw_videos:
            document = self.__parse_video(channel_name, raw_video)

            self.videos_collection.update_one({'video_id': document['video_id']}, {'$set': document}, upsert=True)
        
    def research_channel(self, channel_name):
        channel = models.Channel(channel_name)
        channel.get()
        self.session = channel.session
        pack_iter = channel.iter_all_videos()
        token = channel._continuationToken
        channel.browse(token)

        pass

    def get_video(self, video_id, update_db=True):
        watch = models.Watch(video_id, self.session)
        microformat = watch.get_video()

        document = self.video_document_example.copy()

        document['video_id'] = video_id
        document['username'] = microformat['ownerProfileUrl'].split('@')[1]
        document['channel_id'] = microformat['externalChannelId']
        document['title'] = microformat['title']['simpleText']
        document['thumbnail'] = microformat['thumbnail']
        document['description'] = microformat['description']['simpleText']
        document['durationMs'] = int(microformat['lengthSeconds']) * 1000
        document['viewsCount'] = int(microformat['viewCount'])
        document['publishDate'] = datetime.datetime.strptime(microformat['publishDate'], '%Y-%m-%d')
        document['uploadDate'] = datetime.datetime.strptime(microformat['uploadDate'], '%Y-%m-%d')
        document['category_vector'] = {"category": microformat['category']}

        if update_db:
            result = self.videos_collection.update_one({"video_id": video_id}, {"$set": document}, upsert=True)
            print(result.raw_result)
            
        
        return document
    
    def get_watches_async(self, videos_id_array) -> list[models.Watch]:
        watches_array: list[models.Watch] = []
        video_ids_binds = {}
        get_requests = []

        print("Get watches #1")

        for video_id in videos_id_array:
            watch = models.Watch(video_id, self.session)
            video_ids_binds[video_id] = watch
            watches_array.append(watch)
            get_requests.append(watch.get_async_request())
        
        print("Get watches #2")
        
        for result in grequests.imap(get_requests, size=16):

            html = result.text
            scripts = models.Watch.get_scripts(html)
            url_data = result.request.url
            json_data = models.Watch.search_within_scripts("getTranscriptEndpoint", scripts) # Need to be refactored
            print("Get watches #2.N")
            
            video_ids_binds[url_data.split('=')[1]].json_data = json_data
            print(video_ids_binds[url_data.split('=')[1]].video_id)

        print("Get watches #3")

        return watches_array

    def get_transcription(self, watch: models.Watch):
        return watch.get_transcription()
    
    def get_transcriptions_async(self, watches_array: list[models.Watch]):
        get_transcription_requests = []
        transcriptions_array = []
        modified_transcriptions = []

        # for watch in watches_array:
        #     print(watch)
        #     video_ids_binds[watch.video_id] = watch
        #     get_requests.append(watch.get_async_request())

        # for video_id in video_ids_array:
        #     watch = models.Watch(video_id)
        #     video_ids_binds[video_id] = watch
        #     watches_array.append(watch)
        #     get_requests.append(watch.get_async_request())
        
        # for result in grequests.imap(get_requests, size=16):
        #     html = result.text
        #     url_data = result.request.url
        #     json_data = models.Watch.search_within_scripts("getTranscriptEndpoint", html)
            
        #     video_ids_binds[url_data.split('=')[1]].json_data = json_data # Need to be refactored

        print("Get transcription #1")

        for watch in watches_array:
            transcription_async_request = watch.get_transcription_async_request()
            print(watch.video_id)
            if transcription_async_request != None:
                print(transcription_async_request)
                get_transcription_requests.append(transcription_async_request)
            else:
                print(f"https://youtube.com/{watch.video_id} doesn't has transcriptions")

        print("Get transcription #2")

        for transcription_result in grequests.imap(get_transcription_requests, size=16):
            transcription = json.loads(transcription_result.text)['actions'][0]['updateEngagementPanelAction']['content']['transcriptRenderer']
            transcriptions_array.append(transcription)
            try:
                video_id = json.loads(transcription_result.request.body)['context']['client']['originalUrl'].split('=')[1]
                result = self.update_transcription(transcription, video_id)
                if result.upserted_id != None:
                    modified_transcriptions.append(result.upserted_id)
            except TypeError:
                print("error")

        print("Get transcription #3")

        return modified_transcriptions
    
    def update_transcription(self, transcription, video_id):
        segments = transcription['content']['transcriptSearchPanelRenderer']['body']['transcriptSegmentListRenderer']['initialSegments']
        original_id = self.videos_collection.find_one({'video_id': video_id})['_id']
        if original_id == None:
            self

        body = []
        for segment in segments:
            segment: dict

            segment_renderer_type = list(segment.keys())[0]
            try:
                if segment_renderer_type == 'transcriptSectionHeaderRenderer':
                    text = segment[segment_renderer_type]['snippet']['simpleText']
                elif segment_renderer_type == 'transcriptSegmentRenderer':
                    text = segment[segment_renderer_type]['snippet']['runs'][0]['text']
                
                startMs = segment[segment_renderer_type]['startMs']
                endMs = segment[segment_renderer_type]['endMs']

                line = {
                    "startMs": int(startMs),
                    "endMs": int(endMs),
                    "text": text
                }

                body.append(line)
            except:
                print("ERROR line")
                print(segment_renderer_type)
                print(segment)

        document = {
            "original_id": original_id,
            "transcription": body
        }

        return self.transcriptions_collection.update_one({'original_id': original_id}, {'$set': document}, upsert=True)  

    def find_word(self, word, range_pipeline=[]):
        pipeline = [
            {
                '$match': {
                    'transcription.text': {
                        '$regex': re.compile(word)
                    }
                }
            }, {
                '$project': {
                    'original_id': 1,
                    'transcription': {
                        '$filter': {
                            'input': '$transcription', 
                            'as': 'line', 
                            'cond': {
                                '$regexMatch': {
                                    'input': '$$line.text', 
                                    'regex': re.compile(word)
                                }
                            }
                        }
                    }
                }
            }, {
                '$lookup': {
                    'from': self.videos_collection.name,
                    'localField': 'original_id', 
                    'foreignField': '_id',
                    'pipeline': range_pipeline,
                    'as': 'video'
                }
            }, {
                '$unwind': '$video'
            }
        ]
        return self.transcriptions_collection.aggregate(pipeline)
    
    def __parse_video(self, channel_name, video):
        video_renderer = video['content']['videoRenderer']
        try:
            description = video_renderer['descriptionSnippet']['runs'][0]['text']
        except:
            description = "" 
        text_time = video_renderer['lengthText']['simpleText']
        duration = strToMs(text_time) * 1000


        document = self.video_document_example.copy()
        document['username'] = channel_name
        document['video_id'] = video_renderer['videoId']
        document['title'] = video_renderer['title']['runs'][0]['text']
        document['thumbnail'] = video_renderer['thumbnail']
        document['description'] = description
        document['durationMs'] = duration
        document['durationText'] = text_time

        return document

    def __connect_collections(self): 
        # may be error?
        try:
            self.videos_collection = self.videolang_db.create_collection('videos2')
            self.videos_collection.create_index(('video_id', pymongo.TEXT), unique=True, particialFilterExpressiom={"video_id": {"$not": {"$eq": ""}}})
            self.categories_collaction = self.videolang_db.create_collection('categories')
            self.transcriptions_collection = self.videolang_db.create_collection('transcriptions2')
            self.authors_collection = self.videolang_db.create_collection('authors')
            self.deprecated_videos_collection = self.videolang_db.create_collection('deprecated_videos')
        except:
            self.videos_collection = self.videolang_db.get_collection('videos2')
            self.categories_collaction = self.videolang_db.get_collection('categories')
            self.transcriptions_collection = self.videolang_db.get_collection('transcriptions2')
            self.authors_collection = self.videolang_db.get_collection('authors')
            self.deprecated_videos_collection = self.videolang_db.get_collection('deprecated_videos')
