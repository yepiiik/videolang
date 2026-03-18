import controllers
import grequests
import pymongo
import models

from bson import json_util

client = pymongo.MongoClient("mongodb://localhost:27017/")

if __name__ == "__main__":
    channel = models.Channel('hubermanlab')
    channel.get()
    channel.get_all_videos()
    