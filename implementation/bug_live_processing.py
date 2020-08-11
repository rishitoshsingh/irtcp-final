from pyspark import SparkConf, SparkContext
from pyspark.mllib.classification import  NaiveBayesModel
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.mllib.feature import HashingTF
from pyspark.mllib.feature import IDF
from pyspark.mllib.regression import LabeledPoint

from pymongo import MongoClient
import datetime
from pprint import pprint

import operator
import pickle
import json
import MySQLdb

mongo_username =  'rishi'
mongo_password = 'itsroot'
mongo_host = 'localhost'
mongo_port = 27017

try:
    client = MongoClient('mongodb://{}:{}@{}:{}'.format(mongo_username,mongo_password,mongo_host,str(mongo_port)))
    db = client.irtcp
except:
    print("Database connection unsuccessful!!")
finally:
    client.close()


def insert_tweet(tweet,username,pnr,prediction,tweet_id):
    
    document = {"tweet_id":tweet_id,
                "tweet":tweet,
                "username":username,
                "pnr":pnr,
                "date": datetime.datetime.utcnow()}
    
    if(predict==0):
        try:
            inserted_object = db.feedback.insert_one(tweet).inserted_id    
            print('Inserted : ', inserted_object)
        except:
            print('document insertion FAILED')
    else:
        try:
            inserted_object = db.emergency.insert_one(tweet).inserted_id    
            print('Inserted : ', inserted_object)
        except:
            print('document insertion FAILED')
        
        

from pyspark.streaming import StreamingContext
conf = SparkConf().setMaster("local[2]").setAppName("Streamer")
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")
val = sc.parallelize("abd")


ssc = StreamingContext(sc, 10)
ssc.checkpoint("checkpoint")
kstream = KafkaUtils.createDirectStream(
ssc, topics = ['twitterstream'], kafkaParams = {"metadata.broker.list": 'localhost:9092'})
tweets = kstream.map(lambda x: json.loads(x[1]))

import joblib
loadedModel = joblib.load('IRmodel_joblib')
#with open('IRModel', 'rb') as f:
    #loadedModel = pickle.load(f)

bc_model = sc.broadcast(loadedModel)


def process_data(data):

        print("Processing data ...")        

        if (not data.isEmpty()):
            nbModel=bc_model.value
            hashingTF = HashingTF(100000)
            tf = hashingTF.transform(data.map(lambda x: x[0].encode('utf-8','ignore')))
            tf.cache()
            idf = IDF(minDocFreq=2).fit(tf)
            tfidf = idf.transform(tf)
            tfidf.cache()
            prediction=nbModel.predict(tfidf)

            temp = []
            i=0
            for p,q,r in data.collect():
                temp.append([])
                temp[i].append(p.encode('utf-8','ignore'))
                temp[i].append(q)
                temp[i].append(r)
                i+=1
            i=0
            for p in prediction.collect():
                temp[i].append(p)
                i+=1		

            print(temp)
            for i in temp:
                insert_tweet(str(i[0]),str(i[1]),"0",int(i[3]),int(i[2]))
        else:
            print("Empty RDD !!!")        
            pass

try:
    txt = tweets.map(lambda tweet: (tweet['text'], tweet['user']['screen_name'], tweet['id']))
except:
    print('ERROR while mapping tweet')

txt.foreachRDD(process_data)

#text = tweet_text.map(lambda x: x.encode('utf-8','ignore'))
#text.foreachRDD(process_data)


ssc.start() 
ssc.awaitTerminationOrTimeout(1000)
ssc.stop(stopGraceFully = True)
