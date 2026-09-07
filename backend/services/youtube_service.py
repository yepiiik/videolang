from typing import Optional
from config import YOUTUBE_PROVIDER
from providers.youtube_provider import YouTubeProvider
from providers.api_provider import YouTubeApiProvider
from providers.scrapetube_provider import ScrapetubeProvider

# Factory to get the default provider based on config
def get_default_provider() -> YouTubeProvider:
    if YOUTUBE_PROVIDER.lower() == "scrapetube":
        return ScrapetubeProvider()
    return YouTubeApiProvider()

async def get_channel_info(url_info: dict, provider: Optional[YouTubeProvider] = None):
    active_provider = provider if provider is not None else get_default_provider()
        
    result = await active_provider.get_channel_info(url_info)
    
    # Fallback to API if scrapetube is blocked (e.g., consent wall)
    if result is None and not isinstance(active_provider, YouTubeApiProvider):
        print("Warning: Default provider failed to fetch channel info. Falling back to YouTube API.")
        result = await YouTubeApiProvider().get_channel_info(url_info)
        
    return result

async def get_channel_videos(url_info: dict, provider: Optional[YouTubeProvider] = None):
    active_provider = provider if provider is not None else get_default_provider()
        
    result = await active_provider.get_channel_videos(url_info)
    
    # Fallback to API if scrapetube is blocked (e.g., consent wall)
    if result is None and not isinstance(active_provider, YouTubeApiProvider):
        print("Warning: Default provider failed to fetch videos. Falling back to YouTube API.")
        result = await YouTubeApiProvider().get_channel_videos(url_info)
        
    return result