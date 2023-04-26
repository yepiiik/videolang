import time
# import pymongo
import config

import models


if __name__ == "__main__":
    # myclient = pymongo.MongoClient(f"mongodb://{config.MONGO_INITDB_ROOT_USERNAME}:{config.MONGO_INITDB_ROOT_PASSWORD}@27017/")
    # print(myclient.list_database_names())

    guide_builder = models.Guide_Builder()
    guide_builder.get()
    
    print(guide_builder.formated_data)
