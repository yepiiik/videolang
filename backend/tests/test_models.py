import pytest
from pydantic import ValidationError
from models.youtube_models import ChannelInfo, VideoInfo


class TestYouTubeModels:
    def test_valid_channel_info(self, sample_channel_dict):
        channel = ChannelInfo(**sample_channel_dict)
        assert channel.channel_id == sample_channel_dict["channel_id"]
        assert channel.title == sample_channel_dict["title"]
        assert channel.subscriber_count == 2300000
        assert channel.video_count == 5400
        assert channel.view_count == 180000000

    def test_channel_info_string_numbers_coerced(self, sample_channel_dict):
        # Pydantic coerces numeric strings to int
        data = sample_channel_dict.copy()
        data["subscriber_count"] = "100"
        data["video_count"] = "50"
        data["view_count"] = "1000"

        channel = ChannelInfo(**data)
        assert channel.subscriber_count == 100
        assert channel.video_count == 50
        assert channel.view_count == 1000

    def test_channel_info_missing_required_fields_raises(self):
        with pytest.raises(ValidationError) as exc_info:
            ChannelInfo(channel_id="UC123", title="Test")  # type: ignore

        errors = exc_info.value.errors()
        missing_fields = {e["loc"][0] for e in errors}
        assert "description" in missing_fields
        assert "thumbnail" in missing_fields
        assert "subscriber_count" in missing_fields

    def test_channel_info_invalid_types_raises(self, sample_channel_dict):
        data = sample_channel_dict.copy()
        data["subscriber_count"] = "not-an-integer"
        with pytest.raises(ValidationError):
            ChannelInfo(**data)

    def test_valid_video_info(self, sample_video_dict):
        video = VideoInfo(**sample_video_dict)
        assert video.video_id == sample_video_dict["video_id"]
        assert video.title == sample_video_dict["title"]
        assert video.published_at == sample_video_dict["published_at"]
        assert video.thumbnail == sample_video_dict["thumbnail"]

    def test_video_info_missing_required_fields_raises(self):
        with pytest.raises(ValidationError) as exc_info:
            VideoInfo(video_id="abc123xyz")  # type: ignore

        errors = exc_info.value.errors()
        missing_fields = {e["loc"][0] for e in errors}
        assert "title" in missing_fields
        assert "description" in missing_fields
        assert "published_at" in missing_fields
        assert "thumbnail" in missing_fields
