import math

from services.embedding_service import create_embedding
from database.mongodb import videos_collection


def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float]
) -> float:
    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
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


def find_best_window(
    query_embedding: list[float],
    chunk: dict,
    context_before: float = 15.0,
    context_after: float = 20.0
):
    windows = chunk.get("windows", [])

    if not windows:
        return None

    best_window = None
    best_score = -1.0

    for window in windows:
        embedding = window.get("embedding", [])

        if not embedding:
            continue

        score = cosine_similarity(
            query_embedding,
            embedding
        )

        if score > best_score:
            best_score = score
            best_window = window

    if best_window is None:
        return None

    anchor = (
        best_window["start"]
        + best_window["end"]
    ) / 2

    target_start = max(
        chunk["start"],
        anchor - context_before
    )

    target_end = min(
        chunk["end"],
        anchor + context_after
    )

    return {
        "start": target_start,
        "end": target_end,
        "text": best_window["text"],
        "score": best_score
    }


def semantic_search(
    query: str,
    limit: int = 5
):
    # Единственный embedding API-вызов
    # во время поиска.
    query_embedding = create_embedding(query)

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
                "chunks": 1
            }
        }
    ]

    results = list(
        videos_collection.aggregate(pipeline)
    )

    formatted_results = []

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

        best_window = find_best_window(
            query_embedding,
            best_chunk
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

    formatted_results.sort(
        key=lambda result:
        result["timestamp_score"],
        reverse=True
    )

    formatted_results = [
        result
        for result in formatted_results
        if result["timestamp_score"] >= 0.50
    ]

    return formatted_results[:limit]