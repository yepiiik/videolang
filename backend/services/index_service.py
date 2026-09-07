from services.youtube_service import get_channel_videos
from services.transcript_service import get_video_transcript
from services.chunking_service import chunk_transcript
from services.embedding_service import create_embeddings

from database.mongodb import (
    save_video,
    video_already_indexed,
    get_video
)


def build_time_windows(
    transcript: list,
    start: float,
    end: float,
    window_duration: float = 12.0,
    overlap_duration: float = 4.0
):
    relevant_parts = []

    for part in transcript:
        part_start = float(part["start"])
        part_end = part_start + float(part["duration"])

        if part_end >= start and part_start <= end:
            relevant_parts.append(part)

    if not relevant_parts:
        return []

    windows = []
    current_parts = []
    window_start = None

    for part in relevant_parts:
        text = part["text"].strip()

        if not text:
            continue

        part_start = float(part["start"])
        part_end = part_start + float(part["duration"])

        if window_start is None:
            window_start = part_start

        current_parts.append(part)

        if part_end - window_start < window_duration:
            continue

        windows.append({
            "start": window_start,
            "end": part_end,
            "text": " ".join(
                p["text"].strip()
                for p in current_parts
            )
        })

        overlap_start = part_end - overlap_duration

        current_parts = [
            p
            for p in current_parts
            if float(p["start"]) >= overlap_start
        ]

        if current_parts:
            window_start = float(current_parts[0]["start"])
        else:
            window_start = None

    if current_parts:
        windows.append({
            "start": float(current_parts[0]["start"]),
            "end": (
                float(current_parts[-1]["start"])
                + float(current_parts[-1]["duration"])
            ),
            "text": " ".join(
                p["text"].strip()
                for p in current_parts
            )
        })

    return windows


def add_window_embeddings(
    transcript: list,
    chunk: dict
):
    windows = build_time_windows(
        transcript,
        chunk["start"],
        chunk["end"],
        window_duration=12.0,
        overlap_duration=4.0
    )

    if not windows:
        return []

    texts = [
        window["text"]
        for window in windows
    ]

    embeddings = create_embeddings(texts)

    embedded_windows = []

    for window, embedding in zip(windows, embeddings):
        embedded_windows.append({
            "start": window["start"],
            "end": window["end"],
            "text": window["text"],
            "embedding": embedding
        })

    return embedded_windows


async def index_single_video(video_data: dict):
    video_id = video_data.get("video_id")
    title = video_data.get("title", "")
    if video_already_indexed(video_id):
        print(f"Skipping {video_id}: already indexed")
        existing_video = get_video(video_id)
        if existing_video:
            frontend_chunks = []
            for ec in existing_video.get("chunks", []):
                windows = ec.get("windows", [])
                if not windows:
                    windows = [{
                        "start": ec.get("start"),
                        "end": ec.get("end"),
                        "text": ec.get("text")
                    }]
                frontend_chunks.append({
                    "start": ec.get("start"),
                    "end": ec.get("end"),
                    "text": ec.get("text"),
                    "windows": [
                        {
                            "start": w.get("start"),
                            "end": w.get("end"),
                            "text": w.get("text")
                        } for w in windows
                    ]
                })

            return {
                "status": "skipped",
                "video": {
                    "video_id": existing_video["video_id"],
                    "title": existing_video["title"],
                    "chunks_count": len(frontend_chunks),
                    "chunks": frontend_chunks
                }
            }
        else:
            return {"status": "failed", "reason": "Already indexed but not found in DB"}

    transcript = await get_video_transcript(video_id)

    if "error" in transcript:
        print(f"Skipping {video_id}: {transcript['error']}")
        return {"status": "failed", "reason": transcript["error"]}

    chunks = chunk_transcript(transcript["transcript"])
    embedded_chunks = []

    for chunk in chunks:
        # Основной embedding chunk.
        chunk_embedding = create_embeddings([chunk["text"]])[0]

        # Более мелкие окна внутри chunk.
        embedded_windows = add_window_embeddings(
            transcript["transcript"],
            chunk
        )

        embedded_chunks.append({
            "start": chunk["start"],
            "end": chunk["end"],
            "text": chunk["text"],
            "embedding": chunk_embedding,
            "windows": embedded_windows
        })

    save_video(video_data, transcript, embedded_chunks)
    
    frontend_chunks = []
    for ec in embedded_chunks:
        frontend_chunks.append({
            "start": ec["start"],
            "end": ec["end"],
            "text": ec["text"],
            "windows": [
                {
                    "start": w["start"],
                    "end": w["end"],
                    "text": w["text"]
                } for w in ec.get("windows", [])
            ]
        })
    
    frontend_video = {
        "video_id": video_id,
        "title": title,
        "chunks_count": len(embedded_chunks),
        "chunks": frontend_chunks
    }

    return {"status": "indexed", "video": frontend_video}

async def index_channel(url_info: dict):
    videos = await get_channel_videos(url_info)

    if not videos:
        return {
            "error": "Channel not found"
        }

    # Пока обрабатываем только первые 5 видео.
    videos = videos[:5]

    indexed = []
    skipped = []
    failed = []
    frontend_videos = []

    for video in videos:
        result = await index_single_video(video)
        
        if result["status"] == "skipped":
            skipped.append({"video_id": video["video_id"], "title": video["title"]})
            if "video" in result:
                frontend_videos.append(result["video"])
        elif result["status"] == "failed":
            failed.append({"video_id": video["video_id"], "reason": result.get("reason")})
        elif result["status"] == "indexed":
            indexed.append(result["video"])
            frontend_videos.append(result["video"])

    return {
        "indexed_videos": len(indexed),
        "skipped_videos": len(skipped),
        "failed_videos": len(failed),
        "indexed": indexed,
        "skipped": skipped,
        "failed": failed,
        "videos": frontend_videos
    }