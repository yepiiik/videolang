from database.mongodb import videos_collection, chunks_collection

def migrate():
    videos = list(videos_collection.find())
    print(f'Migrating {len(videos)} videos...')

    migrated_chunks = 0
    for video in videos:
        chunks = video.get('chunks', [])
        if not chunks:
            continue
            
        chunk_docs = []
        for chunk in chunks:
            chunk_docs.append({
                'video_id': video['video_id'],
                'video_title': video['title'],
                'start': chunk.get('start'),
                'end': chunk.get('end'),
                'text': chunk.get('text'),
                'embedding': chunk.get('embedding'),
                'windows': chunk.get('windows')
            })
            
        if chunk_docs:
            chunks_collection.delete_many({'video_id': video['video_id']})
            chunks_collection.insert_many(chunk_docs)
            migrated_chunks += len(chunk_docs)
            
        videos_collection.update_one(
            {'_id': video['_id']},
            {'$set': {'chunks': []}}
        )

    print(f'Migrated {migrated_chunks} chunks successfully!')

if __name__ == '__main__':
    migrate()
