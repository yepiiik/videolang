from urllib.parse import urlparse, parse_qs


def parse_youtube_url(url: str):
    parsed = urlparse(url)

    host = parsed.netloc.lower()
    path = parsed.path
    query = parse_qs(parsed.query)

    # Playlist
    if "list" in query:
        return {
            "type": "playlist",
            "id": query["list"][0]
        }

    # Short link
    if host == "youtu.be":
        return {
            "type": "video",
            "id": path.strip("/")
        }

    # Normal watch link
    if path == "/watch" and "v" in query:
        return {
            "type": "video",
            "id": query["v"][0]
        }

    # @Channel
    if path.startswith("/@"):
        return {
            "type": "handle",
            "id": path[2:]
        }

    # UCxxxx
    if path.startswith("/channel/"):
        return {
            "type": "channel",
            "id": path.split("/")[-1]
        }

    return None