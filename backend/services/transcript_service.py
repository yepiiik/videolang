import asyncio
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import YouTubeTranscriptApiException


def _get_video_transcript_sync(video_id: str):
    try:
        transcript_list = YouTubeTranscriptApi().list(video_id)
        
        try:
            # First try to get English transcript (manual or auto-generated)
            transcript = transcript_list.find_transcript(['en'])
        except Exception:
            # If no English transcript is available, get the first available one
            transcript = list(transcript_list)[0]
            # Translate it to English if translatable
            if transcript.is_translatable:
                transcript = transcript.translate('en')

        data = transcript.fetch()

        return {
            "video_id": video_id,
            "language": transcript.language_code,
            "transcript": [
                {
                    "text": part.text,
                    "start": part.start,
                    "duration": part.duration
                }
                for part in data
            ]
        }

    except Exception as e:
        return {
            "error": str(e)
        }

async def get_video_transcript(video_id: str):
    return await asyncio.to_thread(_get_video_transcript_sync, video_id)