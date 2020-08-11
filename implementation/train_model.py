import os
import sys

from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.mllib.feature import HashingTF
from pyspark.mllib.feature import IDF
import operator

conf=SparkConf()
conf.set("spark.executor.memory", "1g")
conf.set("spark.cores.max", "2")

conf.setAppName("IRApp")

sc = SparkContext('local', conf=conf)


tweetData = sc.textFile("tweets_cleaned.csv")
#tweetData = sc.textFile("tweets_formatted_data.csv")
fields = tweetData.map(lambda x: x.split(","))
documents = fields.map(lambda x: x[1].lower().split(" "))

documentNames = fields.map(lambda x: x[0])
hashingTF = HashingTF(2**14)
article_hash_value = hashingTF.transform(documents)
article_hash_value.cache()

idf = IDF().fit(article_hash_value)
tfidf = idf.transform(article_hash_value)

xformedData=tweetData.zip(tfidf)
xformedData.cache()
xformedData.collect()[0]

from pyspark.mllib.regression import LabeledPoint
def convertToLabeledPoint(inVal) :
    origAttr=inVal[0].split(",")
    sentiment = 0.0 if origAttr[0] == "feedback" else 1.0
    return LabeledPoint(sentiment, inVal[1])

tweetLp=xformedData.map(convertToLabeledPoint)
tweetLp.cache()
tweetLp.collect()

from pyspark.mllib.classification import NaiveBayes, NaiveBayesModel
model = NaiveBayes.train(tweetLp, 1.0)
predictionAndLabel = tweetLp.map(lambda p: \
    (float(model.predict(p.features)), float(p.label)))
predictionAndLabel.collect()

#Forming confusion matrix
from pyspark.sql import SQLContext
sqlContext = SQLContext(sc)
predDF = sqlContext.createDataFrame(predictionAndLabel.collect(), \
                ["prediction","label"])
predDF.groupBy("label","prediction").count().show()

#saving the model
import joblib
joblib.dump(model,'NB.medel')
