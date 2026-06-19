from services.youtube_service import get_channel_videos
from services.transcript_service import get_video_transcript
import time


def index_channel(query: str):
    videos = get_channel_videos(query)

    if not videos:
        return {
            "error": "Channel not found"
        }

    # Временно индексируем только первые 5 видео
    videos = videos[:5]

    indexed = []
    failed = []

    for video in videos:
        transcript = get_video_transcript(video["video_id"])

        if "error" in transcript:
            print(f"Skipping {video['video_id']}: {transcript['error']}")
            failed.append({
                "video_id": video["video_id"],
                "reason": transcript["error"]
            })
            continue

        indexed.append({
            "video": video,
            "transcript": transcript
        })

        time.sleep(1)  # Добавляем задержку между запросами, чтобы избежать превышения лимита

    return {
        "indexed_videos": len(indexed),
        "failed_videos": len(failed),
        "failed": failed,
        "videos": indexed
    }