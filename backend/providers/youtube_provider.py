from abc import ABC, abstractmethod
from typing import Optional


class YouTubeProvider(ABC):
    @abstractmethod
    def get_channel_id(self, url_info: dict) -> Optional[str]:
        """
        Retrieves the channel ID based on the parsed URL info.
        url_info is expected to have 'type' ('channel' or 'channel_handle') and 'id'.
        """
        pass

    @abstractmethod
    async def get_channel_info(self, url_info: dict) -> Optional[dict]:
        """
        Retrieves channel metadata.
        Returns a dict matching models.ChannelInfo shape or None if not found.
        """
        pass

    @abstractmethod
    async def get_channel_videos(self, url_info: dict) -> Optional[list[dict]]:
        """
        Retrieves the recent videos for a channel.
        Returns a list of dicts matching models.VideoInfo shape or None if channel not found.
        """
        pass
