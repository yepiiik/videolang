import models
import controllers

import pymongo
import time
import config
import json
import os
import re


if __name__ == "__main__":
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    controller = controllers.VideolangController(mongo_client=client)

    videos = controller.fast_get_channel_videos("whiskeyblueslounge")
    print(videos)

    # guide_builder = models.Guide_Builder()
    # guide_builder.get()

    # for video in videos_collection.find({"author": "anykadavaika"}):
    #     original_id = video['_id']
    #     if transcriptions_collection.find_one({'original_id': original_id}) != None:
    #         continue
    #     video_id = video['content']['videoRenderer']['videoId']
    #     watch = models.Watch(video_id)
    #     transctiption = watch.get_transcription()
    #     if transctiption == None:
    #         continue
    #     data = {
    #         "content": transctiption['actions'][0]['updateEngagementPanelAction']['content']['transcriptRenderer']['content'],
    #         "original_id": original_id
    #     }
    #     transcriptions_collection.insert_one(data)

    # channel = models.Channel("MrMaxLife")
    # channel.get()
    # channel.get_all_videos()
    # for video in channel.videos:
    #     data = {
    #         "content": video["content"],
    #         "author": channel.channel_name
    #     }
    #     database.videos_collection.insert_one(data)

    # for category in guide_builder.formated_data:
    #     category_title = category['title']
    #     category_channels = category['channels']

    #     for channel_info in category_channels:
    #         username = channel_info['username']
    #         channel = models.Channel(username)
    #         channel.get()
    #         channel.get_all_videos()
    #         for video in channel.videos:
    #             data = {
    #                 "content": video["content"],
    #                 "author": channel.channel_name
    #             }
    #             videos_collection.insert_one(data)
        
    # channel = models.Channel("CHRISHERIA")
    # channel.get()
    # channel.get_all_videos()

    # with open(f"{os.path.dirname(__file__)}/data/{channel.channel_name}.json", "w", encoding="utf8") as file:
    #     data = {
    #         "channel": channel.channel_name,
    #         "videos": {
    #                 "videosCount": len(channel.video_ids),
    #                 "list": channel.videos
    #             }
    #     }
    #     file.write(json.dumps(data))

