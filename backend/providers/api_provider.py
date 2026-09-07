from typing import Optional
from googleapiclient.discovery import build

from config import YOUTUBE_API_KEY
from providers.youtube_provider import YouTubeProvider


class YouTubeApiProvider(YouTubeProvider):
    def __init__(self):
        self.youtube = build(
            "youtube",
            "v3",
            developerKey=YOUTUBE_API_KEY
        )

    def get_channel_id(self, url_info: dict) -> Optional[str]:
        if url_info["type"] == "channel":
            return url_info["id"]

        if url_info["type"] == "channel_handle":
            request = self.youtube.channels().list(
                part="id",
                forHandle=url_info["id"]
            )
            response = request.execute()
            items = response.get("items", [])

            if not items:
                return None

            return items[0]["id"]

        return None

    def get_channel_info(self, url_info: dict) -> Optional[dict]:
        channel_id = self.get_channel_id(url_info)

        if channel_id is None:
            return None

        request = self.youtube.channels().list(
            part="snippet,statistics",
            id=channel_id
        )
        response = request.execute()
        items = response.get("items", [])

        if not items:
            return None

        channel = items[0]

        return {
            "channel_id": channel_id,
            "title": channel["snippet"]["title"],
            "description": channel["snippet"]["description"],
            "thumbnail": channel["snippet"]["thumbnails"]["high"]["url"],
            "subscriber_count": int(
                channel["statistics"].get("subscriberCount", 0)
            ),
            "video_count": int(
                channel["statistics"].get("videoCount", 0)
            ),
            "view_count": int(
                channel["statistics"].get("viewCount", 0)
            )
        }

    def _get_uploads_playlist_id(self, channel_id: str) -> Optional[str]:
        request = self.youtube.channels().list(
            part="contentDetails",
            id=channel_id
        )
        response = request.execute()
        items = response.get("items", [])

        if not items:
            return None

        return items[0]["contentDetails"]["relatedPlaylists"]["uploads"]

    def get_channel_videos(self, url_info: dict) -> Optional[list[dict]]:
        channel_id = self.get_channel_id(url_info)

        if channel_id is None:
            return None

        playlist_id = self._get_uploads_playlist_id(channel_id)

        if playlist_id is None:
            return None

        request = self.youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50
        )
        response = request.execute()
        videos = []

        for item in response.get("items", []):
            snippet = item["snippet"]

            videos.append({
                "video_id": snippet["resourceId"]["videoId"],
                "title": snippet["title"],
                "description": snippet["description"],
                "published_at": snippet["publishedAt"],
                "thumbnail": snippet["thumbnails"]["high"]["url"]
            })

        return videos
