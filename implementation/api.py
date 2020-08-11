from flask import Flask, request
from bson import json_util, ObjectId
import json
import requests
from pymongo import MongoClient
import datetime
from pprint import pprint

app = Flask(__name__)

@app.route('/feedback',methods=['GET'])
def feedback():
    try:
        client = MongoClient("mongodb+srv://rishi:password@irtcpdb-vdq17.mongodb.net/test?retryWrites=true&w=majority")
        db = client.irtcp
        documents = db.feedback.find({})
    except:
        print('Connection Failed')
        return
    finally:
        client.close()
    return {'status':200,
            'data':list(json.loads(json_util.dumps(documents)))}
        

@app.route('/emergency',methods=['GET'])
def feedback():
    try:
        client = MongoClient("mongodb+srv://rishi:password@irtcpdb-vdq17.mongodb.net/test?retryWrites=true&w=majority")
        db = client.irtcp
        documents = db.emergency.find({})
    except:
        print('Connection Failed')
        return
    finally:
        client.close()
    return {'status':200,
            'data':list(json.loads(json_util.dumps(documents)))}
                
        
if __name__=='__main__':
   app.run(debug=True)
   
