from dotenv import load_dotenv
load_dotenv()

import pymongo
import os 
import json

CONNECTION_STR = os.getenv("MONGODB_URI")

client = pymongo.MongoClient(CONNECTION_STR)

db = client.devdb
print(db.name)