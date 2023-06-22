from flask import Flask

import json
import models


app = Flask(__name__)

@app.route("/channel/@<string:channel_name>")
def get_channel_info(channel_name):
    channel = models.Channel(channel_name)
    channel.get()
    channel.get_all_videos()
    data = {
            "channel": channel.channel_name,
            "videos": {
                    "videosCount": len(channel.video_ids),
                    "list": channel.videos
                }
        }
    return json.dumps(data)


if __name__ == "__main__":
    app.run("0.0.0.0", 5000)

