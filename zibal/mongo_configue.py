import pymongo
import pprint
client = pymongo.MongoClient("mongodb://localhost:27017/")
client = pymongo.MongoClient(host="localhost", port=27017)
db = client.zibal

