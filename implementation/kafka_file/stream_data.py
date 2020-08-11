from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import KafkaProducer, KafkaClient
import json

access_token = "Insert your key"
access_token_secret =  "Insert your key"
consumer_key =  "Insert your key"
consumer_secret =  "Insert your key"


class StdOutListener(StreamListener):
    def on_data(self, data):
        decoded = json.loads(data)
        if decoded['text'].startswith('RT'):
            return True
        
        producer.send("twitterstream", data.encode('utf-8','ignore'))
        
        try:
            #pprint(data)
            print(decoded["text"])
        except:
           pass
        return True

kafka = KafkaClient('localhost:9092')
producer = KafkaProducer()
l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, l)#, tweet_mode='extended')
#stream.filter(track=['covid-19','coronavirus','china','corona'], stall_warnings=True, languages = ['en'])

stream.filter(track=['RailwaySeva','indian railways','RailMinIndia','indian railway','irctc','indianrailway18','IRCTCofficial' ], stall_warnings=True, languages = ['en'])

#stream.filter(track=['#test'], stall_warnings=True, languages = ['en'])

