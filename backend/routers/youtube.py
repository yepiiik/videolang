from fastapi import APIRouter

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