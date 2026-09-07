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
chunks_collection = database["chunks"]


def test_connection():
    client.admin.command("ping")
    return True


def video_already_indexed(video_id: str) -> bool:
    existing_video = videos_collection.find_one(
        {"video_id": video_id},
        {"_id": 1}
    )

    return existing_video is not None


def get_video(video_id: str) -> dict:
    video = videos_collection.find_one(
        {"video_id": video_id},
        {"_id": 0}
    )
    if not video:
        return None
        
    chunks_cursor = chunks_collection.find(
        {"video_id": video_id},
        {"_id": 0, "embedding": 0, "windows.embedding": 0}
    ).sort("start", 1)
    
    video["chunks"] = list(chunks_cursor)
    return video


def save_video(video: dict, transcript: dict, chunks: list):
    document = {
        "video_id": video["video_id"],
        "title": video["title"],
        "description": video.get("description", ""),
        "published_at": video.get("published_at", ""),
        "thumbnail": video.get("thumbnail", ""),
        "language": transcript.get("language"),
        "transcript": transcript.get("transcript", [])
    }

    videos_collection.update_one(
        {"video_id": video["video_id"]},
        {"$set": document},
        upsert=True
    )
    
    chunks_collection.delete_many({"video_id": video["video_id"]})
    
    chunk_docs = []
    for chunk in chunks:
        chunk_docs.append({
            "video_id": video["video_id"],
            "video_title": video["title"],
            "start": chunk.get("start"),
            "end": chunk.get("end"),
            "text": chunk.get("text"),
            "embedding": chunk.get("embedding"),
            "windows": chunk.get("windows")
        })
        
    if chunk_docs:
        chunks_collection.insert_many(chunk_docs)

    return document