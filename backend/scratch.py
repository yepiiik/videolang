import sys
sys.path.append('c:/Users/user/prod/py/videolang/backend')
from providers.api_provider import YouTubeApiProvider
from providers.scrapetube_provider import ScrapetubeProvider

api = YouTubeApiProvider()
scrape = ScrapetubeProvider()

url_info = {"type": "channel_handle", "id": "@veritasium"}

print("API Provider:")
print("Channel Info:", api.get_channel_info(url_info))
print("Videos count:", len(api.get_channel_videos(url_info) or []))

print("\nScrapetube Provider:")
print("Channel Info:", scrape.get_channel_info(url_info))
print("Videos count:", len(scrape.get_channel_videos(url_info) or []))
