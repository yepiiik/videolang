from pymongo import MongoClient
from pymongo.server_api import ServerApi

from config import MONGODB_URI


client = MongoClient(
    MONGODB_URI,
    server_api=ServerApi(
        version="1",
        strict=False,
        deprecation_errors=True
    )
)

database = client["videolang"]
videos_collection = database["videos"]


def test_connection():
    client.admin.command("ping")
    return True


def save_video(video: dict, transcript: dict, chunks: list):
    document = {
        "video_id": video["video_id"],
        "title": video["title"],
        "description": video["description"],
        "published_at": video["published_at"],
        "thumbnail": video["thumbnail"],
        "language": transcript.get("language"),
        "transcript": transcript.get("transcript", []),
        "chunks": chunks
    }

    videos_collection.update_one(
        {"video_id": video["video_id"]},
        {"$set": document},
        upsert=True
    )

    return document