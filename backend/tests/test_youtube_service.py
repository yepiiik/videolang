from unittest.mock import AsyncMock, patch, MagicMock
import pytest

from providers.api_provider import YouTubeApiProvider
from providers.scrapetube_provider import ScrapetubeProvider
from services.youtube_service import (
    get_default_provider,
    get_channel_info,
    get_channel_videos,
)


class TestYouTubeService:
    def test_get_default_provider_scrapetube(self, monkeypatch):
        import config
        monkeypatch.setattr(config, "YOUTUBE_PROVIDER", "scrapetube")
        # Also patch inside services.youtube_service because it imports YOUTUBE_PROVIDER directly
        with patch("services.youtube_service.YOUTUBE_PROVIDER", "scrapetube"):
            provider = get_default_provider()
            assert isinstance(provider, ScrapetubeProvider)

    def test_get_default_provider_api(self, monkeypatch):
        with patch("services.youtube_service.YOUTUBE_PROVIDER", "api"):
            provider = get_default_provider()
            assert isinstance(provider, YouTubeApiProvider)

    def test_get_default_provider_fallback_to_api_on_unknown(self):
        with patch("services.youtube_service.YOUTUBE_PROVIDER", "unknown_provider"):
            provider = get_default_provider()
            assert isinstance(provider, YouTubeApiProvider)

    @pytest.mark.asyncio
    async def test_get_channel_info_success_without_fallback(self, sample_channel_dict):
        mock_provider = MagicMock(spec=ScrapetubeProvider)
        mock_provider.get_channel_info = AsyncMock(return_value=sample_channel_dict)

        url_info = {"type": "channel_handle", "id": "GoogleDevelopers"}
        result = await get_channel_info(url_info, provider=mock_provider)

        assert result == sample_channel_dict
        mock_provider.get_channel_info.assert_awaited_once_with(url_info)

    @pytest.mark.asyncio
    async def test_get_channel_info_fallback_when_scrapetube_returns_none(self, sample_channel_dict):
        mock_scrapetube = MagicMock(spec=ScrapetubeProvider)
        mock_scrapetube.get_channel_info = AsyncMock(return_value=None)

        url_info = {"type": "channel_handle", "id": "GoogleDevelopers"}

        with patch.object(YouTubeApiProvider, "get_channel_info", new_callable=AsyncMock) as mock_api_get_info:
            mock_api_get_info.return_value = sample_channel_dict
            result = await get_channel_info(url_info, provider=mock_scrapetube)

        assert result == sample_channel_dict
        mock_scrapetube.get_channel_info.assert_awaited_once_with(url_info)
        mock_api_get_info.assert_awaited_once_with(url_info)

    @pytest.mark.asyncio
    async def test_get_channel_info_no_fallback_if_provider_is_already_api(self):
        # Create an instance of YouTubeApiProvider whose get_channel_info returns None
        api_provider = YouTubeApiProvider()
        api_provider.get_channel_info = AsyncMock(return_value=None)

        url_info = {"type": "channel", "id": "UC12345"}

        with patch.object(YouTubeApiProvider, "__init__", return_value=None) as mock_init:
            result = await get_channel_info(url_info, provider=api_provider)

            assert result is None
            api_provider.get_channel_info.assert_awaited_once_with(url_info)
            # YouTubeApiProvider() constructor should NOT be called for fallback
            mock_init.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_channel_videos_success_without_fallback(self, sample_video_dict):
        mock_provider = MagicMock(spec=ScrapetubeProvider)
        mock_provider.get_channel_videos = AsyncMock(return_value=[sample_video_dict])

        url_info = {"type": "channel_handle", "id": "RickAstley"}
        result = await get_channel_videos(url_info, provider=mock_provider)

        assert result == [sample_video_dict]
        mock_provider.get_channel_videos.assert_awaited_once_with(url_info)

    @pytest.mark.asyncio
    async def test_get_channel_videos_fallback_to_api(self, sample_video_dict):
        mock_scrapetube = MagicMock(spec=ScrapetubeProvider)
        mock_scrapetube.get_channel_videos = AsyncMock(return_value=None)

        url_info = {"type": "channel_handle", "id": "RickAstley"}

        with patch.object(YouTubeApiProvider, "get_channel_videos", new_callable=AsyncMock) as mock_api_get_videos:
            mock_api_get_videos.return_value = [sample_video_dict]
            result = await get_channel_videos(url_info, provider=mock_scrapetube)

        assert result == [sample_video_dict]
        mock_scrapetube.get_channel_videos.assert_awaited_once_with(url_info)
        mock_api_get_videos.assert_awaited_once_with(url_info)

    @pytest.mark.asyncio
    async def test_get_channel_videos_default_provider_when_none_passed(self, sample_video_dict):
        mock_default_provider = MagicMock(spec=YouTubeApiProvider)
        mock_default_provider.get_channel_videos = AsyncMock(return_value=[sample_video_dict])

        url_info = {"type": "channel", "id": "UC_x5XG1OV2P6uZZ5FSM9Ttw"}

        with patch("services.youtube_service.get_default_provider", return_value=mock_default_provider):
            result = await get_channel_videos(url_info, provider=None)

        assert result == [sample_video_dict]
        mock_default_provider.get_channel_videos.assert_awaited_once_with(url_info)
