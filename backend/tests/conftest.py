import os
import sys
from pathlib import Path
import pytest

# Ensure backend root is on sys.path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# Configure dummy environment variables for tests before any module imports config
os.environ.setdefault("YOUTUBE_API_KEY", "mock_youtube_api_key")
os.environ.setdefault("MONGODB_URI", "mongodb://localhost:27017/test_db")
os.environ.setdefault("OPENROUTER_API_KEY", "mock_openrouter_key")
os.environ.setdefault("YOUTUBE_PROVIDER", "api")
os.environ.setdefault("FIREBASE_PRIVATE_KEY", "mock_private_key")
os.environ.setdefault("FIREBASE_CLIENT_EMAIL", "mock@example.com")
os.environ.setdefault("FIREBASE_PROJECT_ID", "mock_project_id")


@pytest.fixture
def sample_channel_dict():
    return {
        "channel_id": "UC_x5XG1OV2P6uZZ5FSM9Ttw",
        "title": "Google Developers",
        "description": "The official channel for Google developers.",
        "thumbnail": "https://example.com/thumbnail.jpg",
        "subscriber_count": 2300000,
        "video_count": 5400,
        "view_count": 180000000,
    }


@pytest.fixture
def sample_video_dict():
    return {
        "video_id": "dQw4w9WgXcQ",
        "title": "Never Gonna Give You Up",
        "description": "Music video by Rick Astley.",
        "published_at": "2009-10-25T06:57:33Z",
        "thumbnail": "https://example.com/rick.jpg",
    }


@pytest.fixture
def sample_transcript():
    return [
        {"text": "Hello world and welcome to the video.", "start": 0.0, "duration": 4.5},
        {"text": "Today we are learning Python testing.", "start": 4.5, "duration": 5.0},
        {"text": "Unit tests are very important.", "start": 9.5, "duration": 3.0},
        {"text": "They prevent regressions.", "start": 12.5, "duration": 4.0},
    ]
