import models

import time
import pymongo
import config



if __name__ == "__main__":
    myclient = pymongo.MongoClient(f"mongodb://localhost:27017/")

    videolang_db = myclient.get_database('videolang')
    videos_collection = videolang_db.get_collection('videos')

    videos_collection.insert_one({'title': "mongo"})
    print(videos_collection.find_one({'title': 'mongo'}))

    # guide_builder = models.Guide_Builder()
    # guide_builder.get()
    
    # print(guide_builder.formated_data)
