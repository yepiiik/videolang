import math

from services.embedding_service import (
    create_embedding,
    create_embeddings
)

from database.mongodb import videos_collection


def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float]
) -> float:
    dot_product = sum(
        a * b for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(value * value for value in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(value * value for value in vector_b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (
        magnitude_a * magnitude_b
    )


def build_time_windows(
    transcript: list,
    start: float,
    end: float,
    window_duration: float = 15.0,
    overlap_duration: float = 5.0
):
    """
    Build small overlapping windows from the original transcript.
    """

    relevant_parts = []

    for part in transcript:
        part_start = float(part["start"])
        part_end = part_start + float(part["duration"])

        # Keep transcript segments that overlap
        # with the semantic chunk.
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

        # Keep the last few seconds as overlap.
        overlap_start = part_end - overlap_duration

        current_parts = [
            p
            for p in current_parts
            if float(p["start"]) >= overlap_start
        ]

        if current_parts:
            window_start = float(
                current_parts[0]["start"]
            )
        else:
            window_start = None

    # Add the remaining part.
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


def find_best_window(
    query_embedding: list[float],
    transcript: list,
    chunk_start: float,
    chunk_end: float,
    context_before: float = 15.0,
    context_after: float = 20.0
):
    windows = build_time_windows(
        transcript,
        chunk_start,
        chunk_end,
        window_duration=12.0,
        overlap_duration=4.0
    )

    if not windows:
        return None

    texts = [
        window["text"]
        for window in windows
    ]

    window_embeddings = create_embeddings(texts)

    best_window = None
    best_score = -1.0

    for window, embedding in zip(
        windows,
        window_embeddings
    ):
        score = cosine_similarity(
            query_embedding,
            embedding
        )

        if score > best_score:
            best_score = score
            best_window = window

    if best_window is None:
        return None

    # Находим центральную точку наиболее релевантного окна.
    anchor = (
        best_window["start"]
        + best_window["end"]
    ) / 2

    # Расширяем контекст вокруг найденной точки.
    target_start = max(
        chunk_start,
        anchor - context_before
    )

    target_end = min(
        chunk_end,
        anchor + context_after
    )

    relevant_parts = []

    for part in transcript:
        part_start = float(part["start"])
        part_end = (
            part_start
            + float(part["duration"])
        )

        if part_end >= target_start and part_start <= target_end:
            relevant_parts.append(part)

    if not relevant_parts:
        return None

    return {
        "start": float(relevant_parts[0]["start"]),
        "end": (
            float(relevant_parts[-1]["start"])
            + float(relevant_parts[-1]["duration"])
        ),
        "text": " ".join(
            part["text"].strip()
            for part in relevant_parts
        ),
        "score": best_score
    }


def semantic_search(
    query: str,
    limit: int = 5
):
    # 1. Embed user's question.
    query_embedding = create_embedding(query)

    # 2. Find relevant videos/chunks.
    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "chunks.embedding",
                "queryVector": query_embedding,
                "numCandidates": 100,
                "limit": 20
            }
        },
        {
            "$project": {
                "_id": 0,
                "video_id": 1,
                "title": 1,
                "transcript": 1,
                "chunks": 1
            }
        }
    ]

    results = list(
        videos_collection.aggregate(pipeline)
    )

    formatted_results = []

    # 3. For each candidate video, find its best chunk.
    for result in results:
        chunks = result.get("chunks", [])

        if not chunks:
            continue

        best_chunk = None
        best_chunk_score = -1.0

        for chunk in chunks:
            embedding = chunk.get("embedding", [])

            if not embedding:
                continue

            score = cosine_similarity(
                query_embedding,
                embedding
            )

            if score > best_chunk_score:
                best_chunk_score = score
                best_chunk = chunk

        if best_chunk is None:
            continue

        # 4. Refine the timestamp inside the chunk.
        best_window = find_best_window(
            query_embedding,
            result["transcript"],
            best_chunk["start"],
            best_chunk["end"]
        )

        if best_window is None:
            continue

        formatted_results.append({
            "video_id": result["video_id"],
            "title": result["title"],
            "score": best_chunk_score,
            "timestamp_score": best_window["score"],
            "start": best_window["start"],
            "end": best_window["end"],
            "text": best_window["text"]
        })

    # 5. Rank by the precise timestamp match.
    formatted_results.sort(
        key=lambda result: result["timestamp_score"],
        reverse=True
    )

    # 6. Remove very weak matches.
    formatted_results = [
        result
        for result in formatted_results
        if result["timestamp_score"] >= 0.50
    ]

    return formatted_results[:limit]