# -*- coding: utf-8 -*-
"""
Created on Wed Sep 07 13:21:35 2016

@author: 024536
"""

import os
import tdbpy
import csv
import zipfile
import shutil
import datetime
from multiprocessing.dummy import Pool as ThreadPool

pSetting = {
    'szIP':"172.22.137.140",
    'szPort':"20003",
    'szUser':"liyonghan",
    'szPassword':"liyo1234",
    'nTimeOutVal':10,
    'nRetryCount':10,
    'nRetryGap':10
}
pProxySetting = {
#TDB_PROXY_TYPE
#    0 TDB_PROXY_SOCK4
#    1 TDB_PROXY_SOCK4A
#    2 TDB_PROXY_SOCK5
#    3 TDB_PROXY_HTTP11
    'nProxyType':0,
    'szProxyHostIp':"",
    'szProxyPort':"",
    'szProxyUser':"",
    'szProxyPwd':"",
}
DictError = {
      0:"TDB_SUCCESS",          #TDB_SUCCESS = 0,
     -1:"TDB_NETWORK_ERROR",    #网络错误
     -2:"TDB_NETWORK_TIMEOUT",  #网络超时
     -3:"TDB_NO_DATA",          #没有数据
     -4:"TDB_OUT_OF_MEMORY",    #内存耗尽
     -5:"TDB_LOGIN_FAILED",     #登陆失败
    -11:"TDB_INVALID_PARAMS",   #无效的参数
    -10:"TDB_INVALID_CODE_TYPE",#无效的代码类型，比如向TDB_GetFuture传入非期货类型代码，返回之。
    -50:"TDB_WRONG_FORMULA",    #指标公式错误        
}
DictFuture = ["chWindCode","chCode","nDate","nTime","iVolume","iTurover"
             ,"nSettle","nPosition","nCurDelta","chTradeFlag"
             ,"iAccVolume","iAccTurover","nHigh","nLow","nOpen","nPrice"
             ,"nPreClose","nPreSettle","nPrePosition"]
DictFutureAB = ["chWindCode","chCode","nDate","nTime","iVolume","iTurover"
               ,"nSettle","nPosition","nCurDelta","chTradeFlag"
               ,"iAccVolume","iAccTurover","nHigh","nLow","nOpen","nPrice"
               ,"nAskPrice1","nAskPrice2","nAskPrice3","nAskPrice4","nAskPrice5"
               ,"nAskVolume1","nAskVolume2","nAskVolume3","nAskVolume4","nAskVolume5"
               ,"nBidPrice1","nBidPrice2","nBidPrice3","nBidPrice4","nBidPrice5"
               ,"nBidVolume1","nBidVolume2","nBidVolume3","nBidVolume4","nBidVolume5"
               ,"nPreClose","nPreSettle","nPrePosition"]
DictTick = ["chWindCode","chCode","nDate","nTime","nPrice","iVolume","iTurover"
           ,"nMatchItems","nInterest","chTradeFlag","chBSFlag"
           ,"iAccVolume","iAccTurover","nHigh","nLow","nOpen","nPreClose"
           ,"nIndex","nStocks","nUps","nDowns","nHoldLines"]
DictTickAB = ["chWindCode","chCode","nDate","nTime","nPrice","iVolume","iTurover"
             ,"nMatchItems","nInterest","chTradeFlag","chBSFlag"
             ,"iAccVolume","iAccTurover","nHigh","nLow","nOpen","nPreClose"
             ,"nAskPrice1","nAskPrice2","nAskPrice3","nAskPrice4","nAskPrice5"
             ,"nAskPrice6","nAskPrice7","nAskPrice8","nAskPrice9","nAskPrice10"
             ,"nAskVolume1","nAskVolume2","nAskVolume3","nAskVolume4","nAskVolume5"
             ,"nAskVolume6","nAskVolume7","nAskVolume8","nAskVolume9","nAskVolume10"
             ,"nBidPrice1","nBidPrice2","nBidPrice3","nBidPrice4","nBidPrice5"
             ,"nBidPrice6","nBidPrice7","nBidPrice8","nBidPrice9","nBidPrice10"
             ,"nBidVolume1","nBidVolume2","nBidVolume3","nBidVolume4","nBidVolume5"
             ,"nBidVolume6","nBidVolume7","nBidVolume8","nBidVolume9","nBidVolume10"
             ,"nAskAvPrice","nBidAvPrice","iTotalAskVolume","iTotalBidVolume"
             ,"nIndex","nStocks","nUps","nDowns","nHoldLines"]
DictTransaction = ["chWindCode","chCode","nDate","nTime","nIndex"
                  ,"chFunctionCode","chOrderKind","chBSFlag","nTradePrice"
                  ,"nTradeVolume","nAskOrder","nBidOrder"]
DictOrder = ["chWindCode","chCode","nDate","nTime","nIndex","nOrder"
            ,"chOrderKind","chFunctionCode","nOrderPrice","nOrderVolume"]
DictOrderQueue = ["chWindCode","chCode","nDate","nTime","nSide","nPrice"
                 ,"nOrderItems","nABItems","nABVolume"]

reqF = {
    "chCode":"CU1609.SHF",    #证券万得代码(AG1312.SHF)
    "nBeginDate":20160901,    #开始日期（交易日）,为0则从当天，例如20130101
    "nEndDate":20160901,      #结束日期（交易日），小于等于0则和nBeginDate相同
    "nBeginTime":0,           #开始时间：若<=0则从头，格式：（HHMMSSmmm）例如94500000 表示 9点45分00秒000毫秒
    "nEndTime":0,             #结束时间：若<=0则至最后
    "nAutoComplete":0         #自动补齐标志:( 0：不自动补齐，1:自动补齐）
}
reqT = {
    "chCode":"600030.SH",     #证券万得代码(AG1312.SHF)
    "nBeginDate":20160901,    #开始日期（交易日）,为0则从当天，例如20130101
    "nEndDate":20160901,      #结束日期（交易日），小于等于0则和nBeginDate相同
    "nBeginTime":0,           #开始时间：若<=0则从头，格式：（HHMMSSmmm）例如94500000 表示 9点45分00秒000毫秒
    "nEndTime":0,             #结束时间：若<=0则至最后
}    
reqKL = {
    "chCode":"CU1609.SHF",    #证券万得代码(AG1312.SHF)
    "nCQFlag":0,              #除权标志：0 不复权，1 向前复权，2 向后复权
    "nCQDate":0,              #复权日期(<=0:全程复权) 格式：YYMMDD，例如20130101表示2013年1月1日
    "nQJFlag":0,              #全价标志(债券)(0:净价 1:全价)
    "nCycType":0,             #数据周期：0 秒线、1 分钟、2 日线、3 周线、4 月线、5 季线、6 半年线、7 年线、8 tickBar
    "nCycDef":1,              #周期数量：仅当nCycType取值：秒、分钟、日线、周线、月线时，这个字段有效。
    "nAutoComplete":0,        #自动补齐：仅1秒钟线、1分钟线支持这个标志，（不为0：补齐；0：不补齐）
    "nBeginDate":20160901,    #开始日期(交易日，<0:从上市日期开始； 0:从今天开始)
    "nEndDate":20160901,      #结束日期(交易日，<=0:跟nBeginDate一样) 
    "nBeginTime":0,           #开始时间，<=0表示从开始，格式：（HHMMSSmmm）例如94500000 表示 9点45分00秒000毫秒
    "nEndTime":0              #结束时间，<=0表示到结束，格式：（HHMMSSmmm）例如94500000 表示 9点45分00秒000毫秒
}

class tdbapi():
    def __init__(self):
        self.tdbapi = tdbpy.tdbapipy()

    def TDB_ERROR(self,flag):
        if flag not in [0,-3,-10]:
            print DictError[flag]
        return flag
        
    def TDB_Open(self,pSetting):
        loginRes = {}
        self.tdbapi.TDB_Open(pSetting,loginRes)
        return loginRes
        
    def TDB_OpenProxy(self,pSetting,pProxySetting):
        loginRes = {}
        self.tdbapi.TDB_OpenProxy(pSetting,pProxySetting,loginRes)
        return loginRes
    
    def TDB_Close(self):
#        print "TDB_Close"
        self.TDB_ERROR(self.tdbapi.TDB_Close())

    def TDB_GetCodeTable(self, szMarket = 'CF'):
#        szMarket in ['SZ','SH','QH','CF','SHF','CZC','DCE']
        pCodeTable=[]
        flag = self.TDB_ERROR(self.tdbapi.TDB_GetCodeTable(szMarket,pCodeTable))
        return pCodeTable,flag

    def TDB_GetKLine(self,reqKL):
        pData = []
        flag = self.TDB_ERROR(self.tdbapi.TDB_GetKLine(reqKL,pData))
        return pData,flag

    def TDB_GetTickAB(self,reqT):
        pData = []
        flag = self.TDB_ERROR(self.tdbapi.TDB_GetTickAB(reqT,pData))
        return pData,flag
        
    def TDB_GetTick(self,reqT):
        pData = []
        flag = self.TDB_ERROR(self.tdbapi.TDB_GetTick(reqT,pData))
        return pData,flag

    def TDB_GetFutureAB(self,reqF):
        pData = []
        flag = self.TDB_ERROR(self.tdbapi.TDB_GetFutureAB(reqF,pData))
        return pData,flag

    def TDB_GetFuture(self,reqF):
        pData = []
        flag = self.TDB_ERROR(self.tdbapi.TDB_GetFuture(reqF,pData))
        return pData,flag  

    def TDB_GetTransaction(self,reqT):
        pData = []
        flag = self.TDB_ERROR(self.tdbapi.TDB_GetTransaction(reqT,pData))
        return pData,flag
 
    def TDB_GetOrder(self,reqT):
        pData = []
        flag = self.TDB_ERROR(self.tdbapi.TDB_GetOrder(reqT,pData))
        return pData,flag
        
    def TDB_GetOrderQueue(self,reqT):
        pData = []
        flag = self.TDB_ERROR(self.tdbapi.TDB_GetOrderQueue(reqT,pData))
        return pData,flag
        
    def TDB_GetCodeInfo(self,szWindCode="IF1609.CF"):
        pCodeDict = {}
        flag = self.TDB_ERROR(self.tdbapi.TDB_GetCodeInfo(szWindCode,pCodeDict))
        return pCodeDict,flag
        
    def TDB_AddFormula(self,szName,szContent):
        pRes = {}
        flag = self.TDB_ERROR(self.tdbapi.TDB_AddFormula(szName,szContent,pRes))
        return pRes,flag
        
    def TDB_GetFormula(self,szFormulaName):
        pFormula = []
        flag = self.TDB_ERROR(self.tdbapi.TDB_GetFormula(szFormulaName,pFormula))
        return pFormula,flag
        
    def TDB_CalcFormula(self,pReqCalc):
        pResult = {}
        flag = self.TDB_ERROR(self.tdbapi.TDB_CalcFormula(pReqCalc,pResult))
        return pResult,flag
        
    def TDB_DeleteFormula(self,szFormulaName):
        pDelRes = {}
        flag = self.TDB_ERROR(self.tdbapi.TDB_DeleteFormula(self,szFormulaName,pDelRes))
        return pDelRes,flag
#------------------------------------------------------------------------------
# for output convenience
def CsvSave(filepath,filename,fields,data):
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    with open(os.path.join(filepath,filename), 'wb') as csvFile:
        csvWriter = csv.DictWriter(csvFile, fieldnames=fields)
        csvWriter.writerow(dict(zip(fields,fields)))
        csvWriter.writerows(data)

def FileToZip(filepath,filenamezip,isdelete=True):
    if not os.path.exists(filepath):
        return
    with zipfile.ZipFile(filenamezip,'w',zipfile.ZIP_DEFLATED) as filezip:
        for filename in os.listdir(filepath):  
            filezip.write(filepath+os.sep+filename,filename)
    if isdelete:
        shutil.rmtree(filepath)

def getOneDay(inputDict):
#    {'datapath':"E:\\data\\tdb\\",'szMarket':"SHF",'flagDate':datetime.datetime(2016,9,5)}
#    oneday=datetime.timedelta(1)
    datapath = inputDict['datapath']
    szMarket = inputDict['szMarket']
    flagDate = inputDict['flagDate']
    strDate = flagDate.strftime("%Y%m%d")
    intDate = int(strDate)
    print strDate
    testapi = tdbapi()
    testapi.TDB_Open(pSetting)
    codeTable,flagcodeTable = testapi.TDB_GetCodeTable(szMarket)
    filepathFutureAB = os.path.join(datapath,"FutureAB",szMarket,strDate)
    filepathTickAB = os.path.join(datapath,"TickAB",szMarket,strDate)
    reqF['nBeginDate'] = intDate
    reqF['nEndDate'] = intDate
    reqT['nBeginDate'] = intDate
    reqT['nEndDate'] = intDate        
    for codeDict in codeTable:
        reqF['chCode']=codeDict['chWindCode']
        reqT['chCode']=codeDict['chWindCode']
        filename=codeDict['chWindCode'].split(".")[0]+".csv"
#        # Future
#        dataFutureAB,flagFutureAB = testapi.TDB_GetFutureAB(reqF)
#        if flagFutureAB == 0:
#            CsvSave(filepathFutureAB,filename,DictFutureAB,dataFutureAB)
#        elif flagFutureAB == -10:
#            dataTickAB,flagTickAB = testapi.TDB_GetTickAB(reqT)
#            if flagTickAB == 0:
#                CsvSave(filepathTickAB,filename,DictTickAB,dataTickAB)
        # Stock
        dataTickAB,flagTickAB = testapi.TDB_GetTickAB(reqT)
        if flagTickAB == 0:
            CsvSave(filepathTickAB,filename,DictTickAB,dataTickAB)
        elif flagTickAB == -10:
            dataFutureAB,flagFutureAB = testapi.TDB_GetFutureAB(reqF)
            if flagFutureAB == 0:
                CsvSave(filepathFutureAB,filename,DictFutureAB,dataFutureAB)
    testapi.TDB_Close()
    FileToZip(filepathFutureAB,filepathFutureAB+".zip",True)
    FileToZip(filepathTickAB,filepathTickAB+".zip",True)

if __name__ == "__main__":
    testapi = tdbapi()
    testapi.TDB_Open(pSetting)
    codeTable,flagcodeTable = testapi.TDB_GetCodeTable("")
#    dataKLine,flagKLine = testapi.TDB_GetKLine(reqKL)
#    dataFutureAB,flagFutureAB = testapi.TDB_GetFutureAB(reqF)
#    dataFuture,flagFuture = testapi.TDB_GetFuture(reqF)
#    dataTickAB,flagTickAB = testapi.TDB_GetTickAB(reqT)
#    dataTick,flagTick = testapi.TDB_GetTick(reqT)
    testapi.TDB_Close()
#    filepath = "testpy"
#    CsvSave(filepath,"dataFutureAB.csv",DictFutureAB,dataFutureAB)
#    CsvSave(filepath,"dataFuture.csv",DictFuture,dataFuture)
#    CsvSave(filepath,"dataTickAB.csv",DictTickAB,dataTickAB)
#    CsvSave(filepath,"dataTick.csv",DictTick,dataTick)
#    FileToZip(filepath,filepath+".zip",False)
    
#    Batch Run test
#    testapi = tdbapi()
#    testapi.TDB_Open(pSetting)
#    codeTable = testapi.TDB_GetCodeTable("SHF")
#    filepath = "FutureAB\\SHF\\20160901"
#    for codeDict in codeTable:
#        reqF['chCode']=codeDict['chWindCode']
#        filename=codeDict['chWindCode'].split(".")[0]+".csv"
#        dataFutureAB,flagFutureAB = testapi.TDB_GetFutureAB(reqF)
#        if flagFutureAB == 0:
#            CsvSave(filepath,filename,DictFutureAB,dataFutureAB)   
#    testapi.TDB_Close()
#    FileToZip(filepath,filepath+".zip",True)
    
#    dictlist = []
#    datapath = "E:\\data\\tdb\\"
#    szMarket = "CZC"
#    begDate = datetime.datetime(2016,9,7)
#    endDate = datetime.datetime(2014,1,1)
#    oneday=datetime.timedelta(1)
#    for i in range(3000):
#        flagDate = begDate-datetime.timedelta(i)
#        if flagDate>endDate:
#            dictlist.append({'flagDate':flagDate,'datapath':datapath,'szMarket':szMarket})
    
#    # Make the Pool of workers
#    pool = ThreadPool(4) 
#    # Open the urls in their own threads
#    # and return the results
#    results = pool.map(getOneDay, dictlist)
#    #close the pool and wait for the work to finish 
#    pool.close() 
#    pool.join() 
    
#    for j in dictlist:
#        getOneDay(j)
        
        
        