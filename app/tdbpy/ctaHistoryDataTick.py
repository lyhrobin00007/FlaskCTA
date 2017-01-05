# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from tdbapi import tdbapi
import pymongo


def loadData(pSetting,chCode,dataType,begDate,endDate):
    mtdbapi = tdbapi()
    TDB_Open_Dict = mtdbapi.TDB_Open(pSetting)

    #证券万得代码(AG1312.SHF)
    #开始日期（交易日）,为0则从当天，例如20130101
    #结束日期（交易日），小于等于0则和nBeginDate相同
    #开始时间：若<=0则从头，格式：（HHMMSSmmm）例如94500000 表示 9点45分00秒000毫秒
    #结束时间：若<=0则至最后
    #自动补齐标志:( 0：不自动补齐，1:自动补齐）
    req = {"chCode":chCode,
           "nBeginDate":int(begDate.replace('-','')),
           "nEndDate":int(endDate.replace('-','')),
           "nBeginTime":0,
           "nEndTime":0}
           
    begDate = datetime.strptime(begDate,'%Y-%m-%d').date()
    endDate = datetime.strptime(endDate,'%Y-%m-%d').date()
    if dataType in ['FutureAB', 'Future']:
        req['nAutoComplete'] = 0
        TDB_GetDataAB = mtdbapi.TDB_GetFutureAB
    else:
        TDB_GetDataAB = mtdbapi.TDB_GetTickAB
        
    dbName = 'VnTrader_Tick_Db'
    host = 'localhost'
    port = 27017
    client = pymongo.MongoClient(host, port, connectTimeoutMS=3600)
    dbName = 'VnTrader_Tick_Db'
    symbol = chCode.split('.')[0]
    database = client[dbName]
    collection = client[dbName][symbol]
    if symbol not in database.collection_names():
        collection.create_index([('datetime', pymongo.ASCENDING)], unique=True)
    
    for i in range((endDate-begDate).days+1):
        tmpDate = begDate + timedelta(i)
        print tmpDate        
        req["nBeginDate"] = int(tmpDate.isoformat().replace('-',''))
        req["nEndDate"] = int(tmpDate.isoformat().replace('-',''))
        dataList,flag = TDB_GetDataAB(req)
        dataList = tdbapi.cleanDataFutureAB(dataList)
        if len(dataList) == 0:
            continue
        try:
            collection.insert_many(dataList)
        except Exception,e:
            print tmpDate.isoformat()+" "+str(e)
            for d in dataList:
                d.pop('_id')
                flt = {'datetime': d['datetime']}
                collection.update_one(flt, {'$set':d}, upsert=True)
    mtdbapi.TDB_Close()    

    
if __name__ == "__main__":
    pSetting = {
        'szIP':"172.22.137.140",
        'szPort':"20003",
        'szUser':"liyonghan",
        'szPassword':"liyo1234",
        'nTimeOutVal':10,
        'nRetryCount':10,
        'nRetryGap':10
    }
    chCode = "CU.SHF"
    dataType = "FutureAB"
    begDateStr = '2012-01-01'
    endDateStr = '2017-01-03'
    
    loadData(pSetting,chCode,dataType,begDateStr,endDateStr)


