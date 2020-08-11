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
import preprocessor
import re

import operator
import pickle
import json
import dns

mongo_username =  'rishi'
mongo_password = 'itsroot'
mongo_host = 'localhost'
mongo_host = 'mongodb+srv://rishi:itsroot@irtcpdb-vdq17.mongodb.net/test?authSource=admin&replicaSet=irtcpdb-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true'
mongo_port = 27017

def insert_tweet(tweet,username,profile_image,pnr,prediction,tweet_id):
    
    #print('Tweet : ', tweet)
    
    document = {"tweet_id":tweet_id,
                "tweet":tweet,
                "username":username,
                "profile_image_url":profile_image,
                "pnr":pnr,
                "timestamp": datetime.datetime.utcnow()}
    #pprint(document)
    if(prediction==0):
        try:
            #client = MongoClient('mongodb://{}:{}@{}:{}'.format(mongo_username,mongo_password,mongo_host,str(mongo_port)))
            client = MongoClient('mongodb+srv://rishi:itsroot@irtcpdb-vdq17.mongodb.net/test?retryWrites=true&w=majority&connectTimeoutMS=90000')
            db = client.irtcp
            inserted_object = db.feedback.insert_one(document).inserted_id    
            print('Inserted : ', inserted_object)
        except:
            print('document insertion FAILED')
        finally:
            client.close()
    else:
        try:
            #client = MongoClient('mongodb://{}:{}@{}:{}'.format(mongo_username,mongo_password,mongo_host,str(mongo_port)))
            client = MongoClient('mongodb+srv://rishi:itsroot@irtcpdb-vdq17.mongodb.net/test?retryWrites=true&w=majority&connectTimeoutMS=90000')
            db = client.irtcp
            inserted_object = db.emergency.insert_one(document).inserted_id    
            print('Inserted : ', inserted_object)
        except:
            print('document insertion FAILED')
        finally:
            client.close()

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

#with open('IRModel', 'rb') as f:
    #loadedModel = pickle.load(f)
    
import joblib
loadedModel = joblib.load('NB.model')    

bc_model = sc.broadcast(loadedModel)


def process_data(data):

        print("Processing data ...")        

        if (not data.isEmpty()):
            nbModel=bc_model.value
            hashingTF = HashingTF(2**14)
            tf = hashingTF.transform(data.map(lambda x: preprocessor.clean(x[0]).encode('utf-8','ignore')))
            tf.cache()
            idf = IDF(minDocFreq=2).fit(tf)
            tfidf = idf.transform(tf)
            tfidf.cache()
            prediction=nbModel.predict(tfidf)

            temp = []
            i=0
            for p,q,r,s in data.collect():
                temp.append([])
                temp[i].append(p) #.encode('utf-8','ignore'))
                temp[i].append(q)
                temp[i].append(r)
                #if re.search("pnr|PNR", tweet_text) and re.search("\d{10}", tweet_text):
                    #pnr = re.findall("\d{10}", txt)
                #else:
                    #pnr = []
                temp[i].append('0') #PNR
                temp[i].append(s)
                i+=1
            i=0
            for p in prediction.collect():
                temp[i].append(p)
                i+=1

            #print(temp)
            for i in temp:
                insert_tweet(str(i[0]),str(i[1]),str(i[2]),i[3],int(i[5]),str(int(i[4])))
        else:
            print("Empty RDD !!!")        
            pass

def tweet_mapper(tweet):
    
    try:
        #if re.search("pnr|PNR", tweet_text) and re.search("\d{10}", tweet_text):
            #pnr = re.findall("\d{10}", txt)
        #else:
            #pnr = []
        tup = (tweet.extended_tweet['full_text'], tweet['user']['screen_name'], tweet['user']['profile_image_url_https'], tweet['id'])
        print('full text')
        return tup
    except:
        print('no full text')
        return (tweet['text'], tweet['user']['screen_name'], tweet['user']['profile_image_url_https'], tweet['id'])
        

txt = tweets.map(lambda tweet: tweet_mapper(tweet))

txt.foreachRDD(process_data)

#text = tweet_text.map(lambda x: x.encode('utf-8','ignore'))
#text.foreachRDD(process_data)

ssc.start() 
ssc.awaitTerminationOrTimeout(1000)
ssc.stop(stopGraceFully = True)
