from fastapi import APIRouter
from database.mongodb import test_connection
from services.embedding_service import create_embedding

from services.youtube_service import (
    get_channel_info,
    get_channel_videos,
)

from services.transcript_service import (
    get_video_transcript,
)

from services.index_service import index_channel

router = APIRouter(
    prefix="/youtube",
    tags=["YouTube"]
)

@router.get("/embedding/test")
def embedding_test(text: str):
    embedding = create_embedding(text)

    return {
        "text": text,
        "dimensions": len(embedding),
        "embedding": embedding
    }

@router.get("/database/test")
def database_test():
    try:
        test_connection()

        return {
            "status": "success",
            "message": "MongoDB connection is working"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@router.get("/channel")
def get_channel(query: str):
    return get_channel_info(query)


@router.get("/channel/videos")
def get_videos(query: str):
    return get_channel_videos(query)


@router.get("/video/transcript")
def transcript(video_id: str):
    return get_video_transcript(video_id)

@router.post("/index/channel")
def index(query: str):
    return index_channel(query)