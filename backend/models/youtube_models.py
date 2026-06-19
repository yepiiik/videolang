from pydantic import BaseModel


class ChannelInfo(BaseModel):
    channel_id: str
    title: str
    description: str
    thumbnail: str

    subscriber_count: int
    video_count: int
    view_count: int


class VideoInfo(BaseModel):
    video_id: str
    title: str
    description: str
    published_at: str
    thumbnail: str