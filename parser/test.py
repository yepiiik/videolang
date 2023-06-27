import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
videolang_db = client.get_database('videolang')

try:
    videos_collection = videolang_db.create_collection('videos')
    videos2_collection = videolang_db.create_collection('videos2')
    transcriptions_collection = videolang_db.create_collection('transcriptions')
    transcriptions2_collection = videolang_db.create_collection('transcriptions2')
except:
    videos_collection = videolang_db.get_collection('videos')
    videos2_collection = videolang_db.get_collection('videos2')
    # videos_collection.drop()
    transcriptions_collection = videolang_db.get_collection('transcriptions')
    transcriptions2_collection = videolang_db.get_collection('transcriptions2')
    # transcriptions2_collection.drop()
    # transcriptions_collection.drop()

if __name__ == "__main__":
    vidoes = videos_collection.aggregate([
        {
            '$lookup': {
                'from': 'transcriptions', 
                'localField': '_id', 
                'foreignField': 'original_id', 
                'as': 'transcription'
            }
        }, {
            '$unwind': '$transcription'
        }, {
            '$match': {
                'author': 'anykadavaika'
            }
        }
    ])

    for video in vidoes:
        # video = videos_collection.find_one({"_id": transcription['original_id']})
        video_id = video['content']['videoRenderer']['videoId']

        # data = {
        #     "original_id": transcription['original_id'],
        #     "transcription": []
        # }
        text = ''
        transcription = video['transcription']

        for segment in transcription['content']['transcriptSearchPanelRenderer']['body']['transcriptSegmentListRenderer']['initialSegments']:
            segment_type = tuple(segment.keys())[0]
            try:
                line = segment[segment_type]
            except:
                print(transcription['original_id'])
            # data['transcription'].append({
            #     "segment_type": segment_type,
            #     "startMs": int(line['startMs']),
            #     "endMs": int(line['endMs']),
            #     "text": line['snippet']['runs'][0]['text']
            # })
            text += line['snippet']['runs'][0]['text'] + ' '

        with open(f'parser/data/{video_id}.txt', 'w', encoding='utf-8') as file:
            file.write(text)
        
        # print(data)
        # transcriptions2_collection.insert_one(data)


        