import time
import config

import models
import json
import os
import re

from progress.bar import IncrementalBar


def transcript(data):
    transcription = json.loads(data)["actions"][0]["updateEngagementPanelAction"]["content"]["transcriptRenderer"]["content"]["transcriptSearchPanelRenderer"]["body"]["transcriptSegmentListRenderer"]["initialSegments"]
    text = ''
    for sentence in transcription:
        try:
            text = text + sentence["transcriptSegmentRenderer"]["snippet"]["runs"][0]["text"] + " "
        except:
            pass
    return text


def get_videos(channel):
    channel.get_videos_pack()
    while True:
        print(len(channel.video_ids))
        try:
            channel.browse()
        except BaseException:
            break
    print("\n")
    print(channel.video_ids)
    print(len(channel.video_ids))


if __name__ == "__main__":
    # guide_builder = models.Guide_Builder()
    # guide_builder.get()

    # guide_builder.formated_data


    # for category in guide_builder.formated_data:
    #     try:
    #         os.mkdir(f"{os.path.dirname(__file__)}/data/{category['title']}")
    #     except FileExistsError:
    #         pass
    #     for channel_name in category["channels"]:
            
    #         # !!! NEED TO BE CHECKED FOR VALID FOLDER NAME !!!
    #         channel = models.Channel(channel_name["username"])
    #         channel.get()
    #         get_videos(channel)

    #         with open(f"{os.path.dirname(__file__)}/data/{category['title']}/{channel.channel_name}.json", "w") as file:
    #             data = {
    #                 "channel": channel.channel_name,
    #                 "videos": {
    #                         "videosCount": len(channel.video_ids),
    #                         "list": channel.videos
    #                     }
    #             }
    #             file.write(json.dumps(data))


    channel = models.Channel("CHRISHERIA")
    channel.get()
    channel.get_all_videos()

    with open(f"{os.path.dirname(__file__)}/data/{channel.channel_name}.json", "w") as file:
        data = {
            "channel": channel.channel_name,
            "videos": {
                    "videosCount": len(channel.video_ids),
                    "list": channel.videos
                }
        }
        file.write(json.dumps(data))

    # for category in guide_builder.formated_data:
    #     try:
    #         print(category["title"] + "-------------------------")
    #         for channel_data in category["channels"]:
    #             username = channel_data["username"]
    #             os.mkdir(username)
    #             channel.get_videos(channel_data["link"])
    #             for id in channel.video_ids:
    #                 watch.get(id)
    #                 watch.get_transcription()
    #                 text = transcript(watch.transcription)
    #                 with open(f"{username}/video_{id}.json", "w", encoding="utf8") as file:
    #                     file.write(text)
    #     except:
    #         pass
    
    
    # print(channel.html)
