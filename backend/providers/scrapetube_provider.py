import re
import json
import requests
import asyncio
from typing import Optional
import scrapetube

from providers.youtube_provider import YouTubeProvider


class ScrapetubeProvider(YouTubeProvider):
    def _fetch_yt_initial_data_sync(self, url: str) -> Optional[dict]:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            html = response.text
            
            # Find ytInitialData using regex
            match = re.search(r'var ytInitialData = (\{.*?\});</script>', html)
            if match:
                return json.loads(match.group(1))
        except Exception:
            pass
        return None

    async def _fetch_yt_initial_data(self, url: str) -> Optional[dict]:
        return await asyncio.to_thread(self._fetch_yt_initial_data_sync, url)

    async def get_channel_id(self, url_info: dict) -> Optional[str]:
        if url_info["type"] == "channel":
            return url_info["id"]

        url = f"https://www.youtube.com/{url_info['id']}" if url_info["type"] == "channel_handle" else f"https://www.youtube.com/channel/{url_info['id']}"
        data = await self._fetch_yt_initial_data(url)
        
        if data:
            try:
                # Extract channelId from metadata
                return data["metadata"]["channelMetadataRenderer"]["externalId"]
            except KeyError:
                pass
                
        return None

    async def get_channel_info(self, url_info: dict) -> Optional[dict]:
        url = f"https://www.youtube.com/{url_info['id']}" if url_info["type"] == "channel_handle" else f"https://www.youtube.com/channel/{url_info['id']}"
        data = await self._fetch_yt_initial_data(url)
        
        if not data:
            return None
            
        try:
            metadata = data["metadata"]["channelMetadataRenderer"]
            channel_id = metadata.get("externalId")
            title = metadata.get("title", "")
            description = metadata.get("description", "")
            
            # Get the highest resolution avatar
            avatars = metadata.get("avatar", {}).get("thumbnails", [])
            thumbnail = avatars[-1]["url"] if avatars else ""

            # Attempt to parse subscriber count from header (rough approximation)
            header = data.get("header", {}).get("c4TabbedHeaderRenderer", {})
            subscriber_text = header.get("subscriberCountText", {}).get("simpleText", "0")
            
            return {
                "channel_id": channel_id,
                "title": title,
                "description": description,
                "thumbnail": thumbnail,
                "subscriber_count": 0, # Difficult to accurately parse "14.5M subscribers" without complex logic, defaulting to 0
                "video_count": 0,
                "view_count": 0
            }
        except KeyError:
            return None

    def _fetch_channel_videos_sync(self, channel_url: str) -> Optional[list[dict]]:
        videos = []
        try:
            # Get latest 50 videos using scrapetube
            generator = scrapetube.get_channel(channel_url=channel_url, limit=50)
            
            for v in generator:
                try:
                    video_id = v["videoId"]
                    title = v.get("title", {}).get("runs", [{}])[0].get("text", "")
                    description = v.get("descriptionSnippet", {}).get("runs", [{}])[0].get("text", "") if "descriptionSnippet" in v else ""
                    published_at = v.get("publishedTimeText", {}).get("simpleText", "")
                    
                    # Highest res thumbnail
                    thumbnails = v.get("thumbnail", {}).get("thumbnails", [])
                    thumbnail = thumbnails[-1]["url"] if thumbnails else ""
                    
                    videos.append({
                        "video_id": video_id,
                        "title": title,
                        "description": description,
                        "published_at": published_at,
                        "thumbnail": thumbnail
                    })
                except Exception:
                    continue
        except Exception:
            return None
            
        return videos

    async def get_channel_videos(self, url_info: dict) -> Optional[list[dict]]:
        channel_url = f"https://www.youtube.com/{url_info['id']}" if url_info["type"] == "channel_handle" else f"https://www.youtube.com/channel/{url_info['id']}"
            
        return await asyncio.to_thread(self._fetch_channel_videos_sync, channel_url)
