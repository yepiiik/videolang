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


def get_scored_windows(
    query_embedding: list[float],
    chunk: dict,
    context_before: float = 15.0,
    context_after: float = 20.0
):
    windows = chunk.get("windows", [])

    if not windows:
        chunk_embedding = chunk.get("embedding", [])
        score = 0.0
        if chunk_embedding:
            score = cosine_similarity(query_embedding, chunk_embedding)
        return [{
            "start": chunk.get("start", 0),
            "end": chunk.get("end", 0),
            "text": chunk.get("text", ""),
            "score": score
        }]

    scored = []
    for window in windows:
        embedding = window.get("embedding", [])
        if not embedding:
            continue

        score = cosine_similarity(query_embedding, embedding)
        anchor = (window["start"] + window["end"]) / 2

        target_start = max(chunk["start"], anchor - context_before)
        target_end = min(chunk["end"], anchor + context_after)

        scored.append({
            "start": target_start,
            "end": target_end,
            "text": window["text"],
            "score": score
        })
    return scored


def semantic_search(
    query: str,
    limit: int = 5
):
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

    results = list(videos_collection.aggregate(pipeline))
    formatted_results = []

    for result in results:
        chunks = result.get("chunks", [])
        if not chunks:
            continue

        all_windows = []
        for chunk in chunks:
            all_windows.extend(get_scored_windows(query_embedding, chunk))
            
        if not all_windows:
            continue
            
        all_windows.sort(key=lambda w: w["score"], reverse=True)
        top_windows = all_windows[:3]
        
        video_score = top_windows[0]["score"]

        for w in top_windows:
            formatted_results.append({
                "video_id": result["video_id"],
                "title": result["title"],
                "score": video_score,
                "timestamp_score": w["score"],
                "start": w["start"],
                "end": w["end"],
                "text": w["text"]
            })

    formatted_results.sort(
        key=lambda result: result["timestamp_score"],
        reverse=True
    )

    return formatted_results[:limit * 3]