import os
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
MONGODB_URI = os.getenv("MONGODB_URI")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
YOUTUBE_PROVIDER = os.getenv("YOUTUBE_PROVIDER", "api")

FIREBASE_PRIVATE_KEY = os.getenv("FIREBASE_PRIVATE_KEY")
FIREBASE_CLIENT_EMAIL = os.getenv("FIREBASE_CLIENT_EMAIL")
FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")

if not YOUTUBE_API_KEY:
    raise ValueError("YOUTUBE_API_KEY not found in .env")