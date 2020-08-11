from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import pprint
import csv

#access_token = "3050035218-x7KuAMHG3C2Yrk2qbrkMEDKbnN2ogEHrrVSp9Ar"
#access_token_secret =  "un09OqOjQaBDO53e9iAZsqTE2cqMZzPduWNMZndTBnNAe"
#consumer_key =  "UvZkmFhM1wTp5t8MFRFEJiDpj"
#consumer_secret =  "stOmR2FAAlWGEljCH7ccyUqShu97i4H96wBHmWpC5R1GK4zMfe"


access_token = "3050035218-97KbLiJvBAlezGE50Nc0rAYRBq2NSUw52thx7jb"
access_token_secret =  "QWWyzr962jAVS7YJQc9nAsAeMFbcJRK2KTnyRxuCHrYeY"
consumer_key =  "X4USsa9CrvuPtsY1RPDkGQet5"
consumer_secret =  "ktZhZCfV5ebAUmziR8ArOUnutjtfLJTPbG3fcR0ZROE22mgkgm"


class StdOutListener(StreamListener):
    def on_data(self, data):
        decoded = json.loads(data)
        tweet = 'Failed'
        try:
            #pprint(data)
            tweet = decoded.extended_tweet['text']
        except:
            tweet = decoded["text"]
    
        print(tweet)
        clss = input()
        fields = []
        if clss == 'e':
            fields = ['emergency',tweet]
        else : 
            field = ['feedback',tweet]
        with open(r'new_data.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(fields)
    
        return True

l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, l, tweet_mode='extended')
stream.filter(track=['covid-19','coronavirus','china','corona'], stall_warnings=True, languages = ['en'])

#stream.filter(track=['RailwaySeva','indian railways','RailMinIndia','indian railway','irctc','indianrailway18','IRCTCofficial' ], stall_warnings=True, languages = ['en'])

