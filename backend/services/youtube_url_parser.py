from urllib.parse import urlparse, parse_qs


def parse_youtube_url(url: str):
    parsed = urlparse(url.strip())

    host = parsed.netloc.lower()
    path = parsed.path.rstrip("/")
    query = parse_qs(parsed.query)

    # www.youtube.com / youtube.com
    if host in {"youtube.com", "www.youtube.com", "m.youtube.com"}:

        # Playlist:
        # https://www.youtube.com/playlist?list=PL...
        if path == "/playlist" and "list" in query:
            return {
                "type": "playlist",
                "id": query["list"][0]
            }

        # Video:
        # https://www.youtube.com/watch?v=...
        if path == "/watch" and "v" in query:
            return {
                "type": "video",
                "id": query["v"][0]
            }

        # Channel by handle:
        # https://www.youtube.com/@Fireship
        if path.startswith("/@"):
            return {
                "type": "channel_handle",
                "id": path[2:]
            }

        # Channel by ID:
        # https://www.youtube.com/channel/UC...
        if path.startswith("/channel/"):
            return {
                "type": "channel",
                "id": path.split("/channel/", 1)[1]
            }

    # Short video URL:
    # https://youtu.be/VIDEO_ID
    if host == "youtu.be":
        video_id = path.lstrip("/")

        if video_id:
            return {
                "type": "video",
                "id": video_id
            }

    return None