from googleapiclient.discovery import build

from config import YOUTUBE_API_KEY

youtube = build(
    "youtube",
    "v3",
    developerKey=YOUTUBE_API_KEY
)


def get_channel_id(query: str):
    request = youtube.search().list(
        part="snippet",
        q=query,
        type="channel",
        maxResults=1
    )

    response = request.execute()

    items = response.get("items", [])

    if not items:
        return None

    return items[0]["snippet"]["channelId"]


def get_channel_info(query: str):
    channel_id = get_channel_id(query)

    if channel_id is None:
        return None

    request = youtube.channels().list(
        part="snippet,statistics",
        id=channel_id
    )

    response = request.execute()

    if not response["items"]:
        return None

    channel = response["items"][0]

    return {
        "channel_id": channel_id,
        "title": channel["snippet"]["title"],
        "description": channel["snippet"]["description"],
        "thumbnail": channel["snippet"]["thumbnails"]["high"]["url"],
        "subscriber_count": int(channel["statistics"].get("subscriberCount", 0)),
        "video_count": int(channel["statistics"].get("videoCount", 0)),
        "view_count": int(channel["statistics"].get("viewCount", 0))
    }


def get_uploads_playlist_id(channel_id: str):
    request = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    )

    response = request.execute()

    items = response.get("items", [])

    if not items:
        return None

    return items[0]["contentDetails"]["relatedPlaylists"]["uploads"]


def get_playlist_videos(playlist_id: str):
    request = youtube.playlistItems().list(
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


def get_channel_videos(query: str):
    channel_id = get_channel_id(query)

    if channel_id is None:
        return None

    playlist_id = get_uploads_playlist_id(channel_id)

    if playlist_id is None:
        return None

    return get_playlist_videos(playlist_id)