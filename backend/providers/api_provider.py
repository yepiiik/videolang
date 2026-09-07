import httpx
from typing import Optional

from config import YOUTUBE_API_KEY
from providers.youtube_provider import YouTubeProvider


class YouTubeApiProvider(YouTubeProvider):
    def __init__(self):
        self.api_key = YOUTUBE_API_KEY
        self.base_url = "https://www.googleapis.com/youtube/v3"

    async def get_channel_id(self, url_info: dict) -> Optional[str]:
        if url_info["type"] == "channel":
            return url_info["id"]

        if url_info["type"] == "channel_handle":
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/channels",
                    params={
                        "part": "id",
                        "forHandle": url_info["id"],
                        "key": self.api_key
                    }
                )
                data = response.json()
                items = data.get("items", [])

                if not items:
                    return None

                return items[0]["id"]

        return None

    async def get_channel_info(self, url_info: dict) -> Optional[dict]:
        channel_id = await self.get_channel_id(url_info)

        if channel_id is None:
            return None

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/channels",
                params={
                    "part": "snippet,statistics",
                    "id": channel_id,
                    "key": self.api_key
                }
            )
            data = response.json()
            items = data.get("items", [])

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

    async def _get_uploads_playlist_id(self, channel_id: str) -> Optional[str]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/channels",
                params={
                    "part": "contentDetails",
                    "id": channel_id,
                    "key": self.api_key
                }
            )
            data = response.json()
            items = data.get("items", [])

            if not items:
                return None

            return items[0]["contentDetails"]["relatedPlaylists"]["uploads"]

    async def get_channel_videos(self, url_info: dict) -> Optional[list[dict]]:
        channel_id = await self.get_channel_id(url_info)

        if channel_id is None:
            return None

        playlist_id = await self._get_uploads_playlist_id(channel_id)

        if playlist_id is None:
            return None

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/playlistItems",
                params={
                    "part": "snippet",
                    "playlistId": playlist_id,
                    "maxResults": 50,
                    "key": self.api_key
                }
            )
            data = response.json()
            videos = []

            for item in data.get("items", []):
                snippet = item["snippet"]

                videos.append({
                    "video_id": snippet["resourceId"]["videoId"],
                    "title": snippet["title"],
                    "description": snippet["description"],
                    "published_at": snippet["publishedAt"],
                    "thumbnail": snippet["thumbnails"]["high"]["url"]
                })

            return videos
