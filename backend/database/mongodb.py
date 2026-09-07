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


def video_already_indexed(video_id: str) -> bool:
    existing_video = videos_collection.find_one(
        {
            "video_id": video_id,
            "chunks.0.embedding": {"$exists": True}
        },
        {
            "_id": 1
        }
    )

    return existing_video is not None


def get_video(video_id: str) -> dict:
    return videos_collection.find_one(
        {"video_id": video_id},
        {"_id": 0}
    )


def save_video(video: dict, transcript: dict, chunks: list):
    document = {
        "video_id": video["video_id"],
        "title": video["title"],
        "description": video.get("description", ""),
        "published_at": video.get("published_at", ""),
        "thumbnail": video.get("thumbnail", ""),
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