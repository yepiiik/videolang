import os
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
MONGODB_URI = os.getenv("MONGODB_URI")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not YOUTUBE_API_KEY:
    raise ValueError("YOUTUBE_API_KEY not found in .env")