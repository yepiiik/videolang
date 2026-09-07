import math
import time

from services.embedding_service import create_embedding
from database.mongodb import chunks_collection

def cosine_similarity(vector_a, vector_b):
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
    magnitude_a = math.sqrt(sum(value * value for value in vector_a))
    magnitude_b = math.sqrt(sum(value * value for value in vector_b))
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    return dot_product / (magnitude_a * magnitude_b)

def get_best_window(query_embedding, chunk):
    windows = chunk.get("windows", [])
    if not windows:
        return chunk
        
    best_window = windows[0]
    best_score = -1.0
    
    for window in windows:
        embedding = window.get("embedding")
        if not embedding:
            continue
        score = cosine_similarity(query_embedding, embedding)
        if score > best_score:
            best_score = score
            best_window = window
            
    # Include some context around the window
    context_before = 15.0
    context_after = 20.0
    anchor = (best_window["start"] + best_window["end"]) / 2
    target_start = max(chunk["start"], anchor - context_before)
    target_end = min(chunk["end"], anchor + context_after)
    
    return {
        "start": target_start,
        "end": target_end,
        "text": best_window["text"]
    }

def semantic_search(
    query: str,
    limit: int = 5
):
    start_time = time.time()
    query_embedding = create_embedding(query)
    embedding_time = time.time() - start_time

    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": query_embedding,
                "numCandidates": 100,
                "limit": 50
            }
        },
        {
            "$project": {
                "_id": 0,
                "video_id": 1,
                "video_title": 1,
                "start": 1,
                "end": 1,
                "text": 1,
                "windows": 1,
                "score": {"$meta": "vectorSearchScore"}
            }
        },
        {
            "$group": {
                "_id": "$video_id",
                "video_title": {"$first": "$video_title"},
                "chunks": {
                    "$push": {
                        "start": "$start",
                        "end": "$end",
                        "text": "$text",
                        "windows": "$windows",
                        "score": "$score"
                    }
                },
                "max_score": {"$max": "$score"}
            }
        },
        {
            "$sort": {"max_score": -1}
        },
        {
            "$limit": limit
        }
    ]

    vector_search_start = time.time()
    results = list(chunks_collection.aggregate(pipeline))
    vector_search_time = time.time() - vector_search_start

    formatted_results = []

    for result in results:
        top_chunks = sorted(result["chunks"], key=lambda c: c["score"], reverse=True)[:3]
        for chunk in top_chunks:
            best_window = get_best_window(query_embedding, chunk)
            formatted_results.append({
                "video_id": result["_id"],
                "title": result["video_title"],
                "score": result["max_score"],
                "timestamp_score": chunk["score"],
                "start": best_window["start"],
                "end": best_window["end"],
                "text": best_window["text"]
            })

    # Sort results just in case, though Atlas Vector Search already sorts by score
    formatted_results.sort(
        key=lambda r: r["timestamp_score"],
        reverse=True
    )

    total_time = time.time() - start_time
    print(f"Semantic Search Timing:")
    print(f"  - Embedding generation: {embedding_time:.4f}s")
    print(f"  - Vector DB query: {vector_search_time:.4f}s")
    print(f"  - Total execution time: {total_time:.4f}s")

    return formatted_results