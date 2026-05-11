from gevent import monkey
monkey.patch_all()

from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin

from bson import json_util
import controllers

import pymongo



app = Flask(__name__)
CORS(app)

@app.route('/channel')
def get_channel_info():
    keys = list(request.args.keys())
    if 'uuid' in keys:
        channel_name = request.args.get('uuid')
        data = controller.get_uptodate_channel_videos(channel_name)
        return json_util.dumps(data)
    return '405 bad request'

@app.route('/get_videos')
def get_video():
    keys = list(request.args.keys())
    data = []
    if 'c' in keys:
        channels = request.args.getlist('c')
        for channel in channels:
            pipeline = [
                {
                    '$match': {
                        'username': channel
                    }
                }
            ]
            videos = list(controller.videos_collection.aggregate(pipeline))
            data += videos
        return json_util.dumps(data)
    return '405 bad request'

@app.route('/get_transcriptions')
def get_transcriptions():
    data = []
    keys = list(request.args.keys())
    if 'c' in keys:
        channels = request.args.getlist('c')
        for channel in channels:
            pipeline = [
                {
                    '$group': {
                        '_id': '$username', 
                        'videos': {
                            '$addToSet': '$video_id'
                        }
                    }
                }, {
                    '$match': {
                        '_id': channel
                    }
                }
            ]
            try:
                videos_id = list(controller.videos_collection.aggregate(pipeline))[0]['videos']
            except:
                pass
            print(controller.get_uptodate_channel_videos(channel))
            videos_id = list(controller.videos_collection.aggregate(pipeline))[0]['videos']
            watches = controller.get_watches_async(videos_id)
            data.append(controller.get_transcriptions_async(watches))

    return json_util.dumps(data)

@app.route('/get_new')
def get_new():
    data = []
    keys = list(request.args.keys())
    if 'c' in keys:
        channels = request.args.getlist('c')
        for channel in channels:
            pipeline = [
                {
                    '$group': {
                        '_id': '$username', 
                        'videos': {
                            '$addToSet': '$video_id'
                        }
                    }
                }, {
                    '$match': {
                        '_id': channel
                    }
                }
            ]
            old_videos_id = list(controller.videos_collection.aggregate(pipeline))
            print(old_videos_id)
            if old_videos_id != []:
                old_videos_id = old_videos_id[0]['videos']
            controller.update_channel_videos(channel)
            pipeline = [
                {
                    '$match': {
                        'username': channel,
                        'video_id': {'$nin': old_videos_id}
                    }
                }
            ]
            new_videos_id = list(controller.videos_collection.aggregate(pipeline))

    return json_util.dumps(new_videos_id)

@app.route('/update_content')
def update_content():
    keys = list(request.args.keys())
    if 'c' in keys:
        channel_name = request.args.get('c')
        controller.videos_collection.aggregate


@app.route('/find_text')
def find_text():
    range_pipeline = []

    keys = list(request.args.keys())
    if 'q' not in keys:
        return "400 Bad request"
    if 'c' in keys:
        channels = request.args.getlist('c')
        range_pipeline = [
            {
                '$match': {
                    'username': {
                        '$in': channels
                    }
                }
            }
        ]
    word = request.args.get('q')
    data = controller.find_word(word, range_pipeline)
    return json_util.dumps(data)

@app.route('/fast_find_text')
def fast_find_text():
    range_pipeline = []
    keys = list(request.args.keys())

    if 'c' in keys:
        channels = request.args.getlist('c')
        range_pipeline = [
            {
                '$match': {
                    'username': {
                        '$in': channels
                    }
                }
            }
        ]

    word = request.args.get('q')
    data = controller.find_word(word, range_pipeline)
    return json_util.dumps(data)

@app.route('/test')
def test():
    keys = list(request.args.keys())
    if 'p' in keys:
        params = request.args.getlist('p')
        return json_util.dumps(params)
    return "empty"

if __name__ == "__main__":
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    controller = controllers.VideolangController(mongo_client=client)
    app.run("0.0.0.0", 5000)

