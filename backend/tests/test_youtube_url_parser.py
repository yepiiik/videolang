import pytest
from services.youtube_url_parser import parse_youtube_url


class TestYouTubeUrlParser:
    @pytest.mark.parametrize(
        "url, expected_id",
        [
            ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://m.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://www.youtube.com/watch?v=dQw4w9WgXcQ&feature=share", "dQw4w9WgXcQ"),
            ("  https://www.youtube.com/watch?v=dQw4w9WgXcQ  ", "dQw4w9WgXcQ"),
            ("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://youtu.be/dQw4w9WgXcQ?t=42", "dQw4w9WgXcQ"),
        ],
    )
    def test_parse_video_urls(self, url, expected_id):
        result = parse_youtube_url(url)
        assert result is not None
        assert result["type"] == "video"
        assert result["id"] == expected_id

    @pytest.mark.parametrize(
        "url, expected_id",
        [
            ("https://www.youtube.com/playlist?list=PLlaN88a7xKIvK-2b2r1N9l9QvC_jYyN", "PLlaN88a7xKIvK-2b2r1N9l9QvC_jYyN"),
            ("https://youtube.com/playlist?list=PL12345&si=abc", "PL12345"),
        ],
    )
    def test_parse_playlist_urls(self, url, expected_id):
        result = parse_youtube_url(url)
        assert result is not None
        assert result["type"] == "playlist"
        assert result["id"] == expected_id

    @pytest.mark.parametrize(
        "url, expected_handle",
        [
            ("https://www.youtube.com/@Fireship", "Fireship"),
            ("https://youtube.com/@mkbhd", "mkbhd"),
            ("https://m.youtube.com/@veritasium", "veritasium"),
        ],
    )
    def test_parse_channel_handle_urls(self, url, expected_handle):
        result = parse_youtube_url(url)
        assert result is not None
        assert result["type"] == "channel_handle"
        assert result["id"] == expected_handle

    @pytest.mark.parametrize(
        "url, expected_channel_id",
        [
            ("https://www.youtube.com/channel/UC_x5XG1OV2P6uZZ5FSM9Ttw", "UC_x5XG1OV2P6uZZ5FSM9Ttw"),
            ("https://youtube.com/channel/UCBCII4A2k-oY", "UCBCII4A2k-oY"),
        ],
    )
    def test_parse_channel_id_urls(self, url, expected_channel_id):
        result = parse_youtube_url(url)
        assert result is not None
        assert result["type"] == "channel"
        assert result["id"] == expected_channel_id

    @pytest.mark.parametrize(
        "invalid_url",
        [
            "https://vimeo.com/123456",
            "https://www.google.com",
            "https://www.youtube.com/feed/subscriptions",
            "https://youtu.be/",
            "not a url at all",
            "",
            "   ",
        ],
    )
    def test_parse_invalid_or_unsupported_urls(self, invalid_url):
        result = parse_youtube_url(invalid_url)
        assert result is None
