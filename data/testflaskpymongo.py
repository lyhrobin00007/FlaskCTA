# -*- coding: utf-8 -*-
"""
Created on Thu Jan 05 11:51:34 2017

@author: 024536
"""

from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_DBNAME'] = "VnTrader_Tick_Db"
mongo = PyMongo()
mongo.init_app(app)


with app.app_context():
    database = mongo.db
    symbols = database.collection_names()
    statDatas = []
    for symbol in symbols:
        statData = {}
        statData['symbol'] = symbol
        statData['begTime'] = database[symbol].find().sort("datetime",1).limit(1)[0]['datetime'].isoformat()
        statData['endTime'] = database[symbol].find().sort("datetime",-1).limit(1)[0]['datetime'].isoformat()
        statDatas.append(statData)
    print statDatas
    
    
    