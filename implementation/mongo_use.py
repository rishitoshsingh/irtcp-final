from pymongo import MongoClient
import datetime
from pprint import pprint

username =  'rishi'
password = 'itsroot'
host = 'localhost'
port = 27017

client = MongoClient('mongodb://{}:{}@{}:{}'.format(username,password,host,str(port)))
db = client.irtcp
collection = db.twitter

tweet = {"test":" 😀 3",
         "tweet_id":1234567890,
         "date": datetime.datetime.utcnow()}
inserted_tweet_id = collection.insert_one(tweet).inserted_id
pprint(tweet)
print('Inserted : ', inserted_tweet_id)

