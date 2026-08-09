from services.youtube_service import get_channel_videos
from services.transcript_service import get_video_transcript
from services.chunking_service import chunk_transcript

from database.mongodb import save_video


def index_channel(query: str):
    videos = get_channel_videos(query)

    if not videos:
        return {
            "error": "Channel not found"
        }

    # Временно обрабатываем только первые 5 видео.
    videos = videos[:5]

    indexed = []
    failed = []

    for video in videos:
        transcript = get_video_transcript(video["video_id"])

        if "error" in transcript:
            print(
                f"Skipping {video['video_id']}: "
                f"{transcript['error']}"
            )

            failed.append({
                "video_id": video["video_id"],
                "reason": transcript["error"]
            })

            continue

        chunks = chunk_transcript(
            transcript["transcript"]
        )

        save_video(
            video,
            transcript,
            chunks
        )

        indexed.append({
            "video_id": video["video_id"],
            "title": video["title"],
            "chunks": len(chunks)
        })

    return {
        "indexed_videos": len(indexed),
        "failed_videos": len(failed),
        "failed": failed,
        "videos": indexed
    }