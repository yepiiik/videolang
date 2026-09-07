from fastapi import APIRouter, HTTPException, Depends
from dependencies.auth import verify_api_key

from services.youtube_url_parser import parse_youtube_url

from services.youtube_service import (
    get_channel_info,
    get_channel_videos,
)

from services.transcript_service import (
    get_video_transcript,
)

from services.index_service import index_channel, index_single_video

from services.search_service import semantic_search

from services.embedding_service import create_embedding

from database.mongodb import test_connection


router = APIRouter(
    prefix="/youtube",
    tags=["YouTube"]
)


@router.get("/channel")
async def get_channel(query: str):
    parsed_url = parse_youtube_url(query)

    if parsed_url is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid YouTube URL"
        )

    if parsed_url["type"] not in {
        "channel",
        "channel_handle"
    }:
        raise HTTPException(
            status_code=400,
            detail="URL must point to a YouTube channel"
        )

    result = await get_channel_info(parsed_url)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Channel not found"
        )

    return result


@router.get("/channel/videos")
async def get_videos(query: str):
    parsed_url = parse_youtube_url(query)

    if parsed_url is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid YouTube URL"
        )

    if parsed_url["type"] not in {
        "channel",
        "channel_handle"
    }:
        raise HTTPException(
            status_code=400,
            detail="URL must point to a YouTube channel"
        )

    result = await get_channel_videos(parsed_url)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Channel not found"
        )

    return result


@router.get("/video/transcript")
async def transcript(video_id: str):
    return await get_video_transcript(video_id)


@router.post("/index/channel")
async def index(query: str):
    parsed_url = parse_youtube_url(query)

    if parsed_url is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid YouTube URL"
        )

    if parsed_url["type"] not in {
        "channel",
        "channel_handle"
    }:
        raise HTTPException(
            status_code=400,
            detail="URL must point to a YouTube channel"
        )

    return await index_channel(parsed_url)


from pydantic import BaseModel
class IndexVideoRequest(BaseModel):
    video_id: str
    title: str
    description: str = ""
    published_at: str = ""
    thumbnail: str = ""

@router.post("/index/video")
async def index_video(request: IndexVideoRequest):
    return await index_single_video(request.model_dump())


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


@router.get("/embedding/test")
def embedding_test(text: str):
    embedding = create_embedding(text)

    return {
        "text": text,
        "dimensions": len(embedding),
        "embedding": embedding
    }


@router.get("/search")
def search(query: str, api_key: str = Depends(verify_api_key)):
    return semantic_search(query)