from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import YouTubeTranscriptApiException


def get_video_transcript(video_id: str):
    try:

        transcript = YouTubeTranscriptApi().fetch(video_id)

        return {
            "video_id": video_id,
            "language": transcript.language_code,
            "transcript": [
                {
                    "text": part.text,
                    "start": part.start,
                    "duration": part.duration
                }
                for part in transcript
            ]
        }

    except YouTubeTranscriptApiException as e:
        return {
            "error": str(e)
        }