from flask import Flask

from bson import json_util
import controllers

import pymongo


app = Flask(__name__)

@app.route("/channel/@<string:channel_name>")
def get_channel_info(channel_name):
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    controller = controllers.VideolangController(mongo_client=client)
    data = controller.get_uptodate_channel_videos(channel_name)
    return json_util.dumps(data)


if __name__ == "__main__":
    app.run("0.0.0.0", 5000)

