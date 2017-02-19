# -*- coding: utf-8 -*-

import os
import zipfile
from datetime import datetime
from ctaBase import *
from vtFunction import loadMongoSetting
import pymongo

dbName = 'VnTrader_Tick_Db'
host, port = loadMongoSetting()
client = pymongo.MongoClient(host, port)

import logging

logger=logging.getLogger()
handler=logging.FileHandler("Log_ctaHistoryDataTick.txt")
logger.addHandler(handler)
logger.setLevel(logging.NOTSET)
  
def zip2mongodb(filename='20160922.zip'):
    multi = 10000.0
    with zipfile.ZipFile(filename,'r') as filezip:
        filelist = filezip.namelist()
#        print filelist
        for ifile in filelist:
            product = os.path.basename(ifile)
            if product in ['cu.csv','ru.csv','rb.csv','zn.csv']:
#            if product in ['rb.csv']:
                symbol = os.path.basename(ifile).split('.')[0]
#                symbol = 'cu0'
                collection = client[dbName][symbol]
                collection.create_index([('datetime', pymongo.ASCENDING)], unique=True) 
                
                print ifile
                logger.debug(ifile)
                data = filezip.read(ifile).decode('gbk').split('\r\n')
                if data[0][0:4] == 'code':
                    logStr = 'Begin line 1, field type 1'
                    beg = 1
                    fieldtype = 1
                elif data[0][0:4] == 'chWi':
                    logStr = 'Begin line 1, field type 2'
                    beg = 1
                    fieldtype = 2
                else:
                    logStr = 'Begin line 2, field type 1'
                    beg = 2
                    fieldtype = 1
                print logStr
                logger.debug(logStr)
                if fieldtype == 1:
                    fieldnames = data[beg-1].replace(',price,',',lastPrice,')\
                        .replace(',ask',',askPrice').replace(',bid',',bidPrice')\
                        .replace(',asize',',askVolume').replace(',bsize',',bidVolume')\
                        .replace('position','openInterest').replace('turover','turnover')\
                        .replace(',open,',',openPrice,')\
                        .replace(',high,',',highestPrice,').replace(',low,',',lowestPrice,')\
                        .replace(',settle,',',settlementPrice,').replace(',cur_delta,',',currDelta,')\
                        .replace(',pre_openInterest,',',preOpenInterest,').replace(',trade_flag,',',tradeFlag,')\
                        .replace(',pre_close,',',preClosePrice,').replace(',pre_settle,',',preSettlementPrice,')\
                        .replace('wind_code','windCode')\
                        .split(',')
                else:
                    fieldnames = data[beg-1].replace('chWindCode,','windCode,')\
                        .replace(',nD',',d').replace(',nT',',t')\
                        .replace(',nA',',a').replace(',nB',',b')\
                        .replace(',nP',',p').replace(',nS',',s')\
                        .replace(',nC',',c').replace(',chT',',t')\
                        .replace(',iV',',v').replace(',iT',',t')\
                        .replace(',iAccVolume',',accvolume').replace(',iAccTurover',',accturnover')\
                        .replace('nHigh','highestPrice').replace('nLow','lowestPrice')\
                        .replace('nOpen','openPrice').replace(',price,',',lastPrice,')\
                        .replace(',preClose,',',preClosePrice,').replace(',preSettle,',',preSettlementPrice,')\
                        .replace(',prePosition,',',preOpenInterest,').replace('chCode','code')\
                        .replace('position','openInterest').replace('turover','turnover')\
                        .replace(',open,',',openPrice,').replace(',close,',',closePrice,')\
                        .replace(',settle,',',settlementPrice,').replace('prePosition','preOpenInterest')\
                        .replace(',curDelta,',',currDelta,')\
                        .split(',')
                    
                for idata in data[beg:]:
                    if idata == u'':
                        continue
                    
                    d = dict(zip(fieldnames,idata.split(',')))
                    try:
                        d['vtSymbol'] = d['windCode'].split('.')[0]           # vt系统代码
                        d['symbol'] = d['windCode'].split('.')[0]            # 合约代码
                        d['exchange'] = u''                       # 交易所代码    
            
                        # 成交数据
                        d['lastPrice'] = float(d['lastPrice'])/multi            # 最新成交价
                        
                        d['volume'] = int(d['accvolume'])                 # 最新成交量
            #            d['accvolume'] = int(d['accvolume'])
                        d.pop('accvolume')
                        d['turnover'] = float(d['accturnover'])
            #            d['accturnover'] = float(d['accturnover'])
                        d.pop('accturnover')
            
                        d['openInterest'] = int(d['openInterest'])           # 持仓量
                        d['preOpenInterest'] = int(d['preOpenInterest'])
                        d['openPrice'] = float(d['openPrice'])/multi
                        d['highestPrice'] = float(d['highestPrice'])/multi
                        d['lowestPrice'] = float(d['lowestPrice'])/multi
                        d['preClosePrice'] = float(d['preClosePrice'])/multi
                        d['settlementPrice'] = float(d['settlementPrice'])/multi
                        d['preSettlementPrice'] = float(d['preSettlementPrice'])/multi
            
            #            self.upperLimit = EMPTY_FLOAT           # 涨停价
            #            self.lowerLimit = EMPTY_FLOAT           # 跌停价
                        
                        # tick的时间
                        d['date'] = d['date']            # 日期
                        
                        d['time'] = u'0'*(9-len(d['time']))+d['time']
                        d['time'] = d['time'][0:2]+':'+d['time'][2:4]+':'+d['time'][4:6]+'.'+d['time'][6:9]         # 时间
#                        print d['date'] + ' ' + d['time']
                        d['datetime'] = datetime.strptime(d['date'] + ' ' + d['time'], '%Y%m%d %H:%M:%S.%f')  # python的datetime时间对象
#                        d['datetime'] = datetime.strptime(d['date'] + ' ' + d['time'], '%Y%m%d %H%M%S%f')  # python的datetime时间对象
#                        print d['datetime']
                        # 五档行情
                        d['bidPrice1'] = float(d['bidPrice1'])/multi
                        d['bidPrice2'] = float(d['bidPrice2'])/multi
                        d['bidPrice3'] = float(d['bidPrice3'])/multi
                        d['bidPrice4'] = float(d['bidPrice4'])/multi
                        d['bidPrice5'] = float(d['bidPrice5'])/multi
                        d.pop('bidPrice2')
                        d.pop('bidPrice3')
                        d.pop('bidPrice4')
                        d.pop('bidPrice5')
                        
                        d['askPrice1'] = float(d['askPrice1'])/multi
                        d['askPrice2'] = float(d['askPrice2'])/multi
                        d['askPrice3'] = float(d['askPrice3'])/multi
                        d['askPrice4'] = float(d['askPrice4'])/multi
                        d['askPrice5'] = float(d['askPrice5'])/multi
                        d.pop('askPrice2')
                        d.pop('askPrice3')
                        d.pop('askPrice4')
                        d.pop('askPrice5')                    
                        
                        d['bidVolume1'] = int(d['bidVolume1'])
                        d['bidVolume2'] = int(d['bidVolume2'])
                        d['bidVolume3'] = int(d['bidVolume3'])
                        d['bidVolume4'] = int(d['bidVolume4'])
                        d['bidVolume5'] = int(d['bidVolume5'])
                        d.pop('bidVolume2')
                        d.pop('bidVolume3')
                        d.pop('bidVolume4')
                        d.pop('bidVolume5')
                        
                        d['askVolume1'] = int(d['askVolume1'])
                        d['askVolume2'] = int(d['askVolume2'])
                        d['askVolume3'] = int(d['askVolume3'])
                        d['askVolume4'] = int(d['askVolume4'])
                        d['askVolume5'] = int(d['askVolume5'])
                        d.pop('askVolume2')
                        d.pop('askVolume3')
                        d.pop('askVolume4')
                        d.pop('askVolume5')
            
                        #other data
                        d['currDelta'] = float(d['currDelta'])
            
                        flt = {'datetime': d['datetime']}
                        collection.update_one(flt, {'$set':d}, upsert=True)
                    except Exception,e:
                        print e
                        print d
                        logger.debug(str(e))
                        logger.debug(d)
#                    print d['date'], d['time']
#                collection.

datapath = 'F:/BaiduYunDownload/SHF/'
years = os.listdir(datapath)
#years = ['2016','2015','2014','2013','2012','2011','2010']
years = ['2016','2015','2014','2013']
for year in years:
    dates = os.listdir(os.path.join(datapath,year))
#    if year == '2016':
#        dates = dates[:100]
#    elif year == '2015':
#        dates = []
#    elif year == '2014':
#        dates = dates[197:]    
    for date in dates[::-1]:
        filename=datapath+year+'/'+date
        print filename
        zip2mongodb(filename)            

#zip2mongodb(datapath+'2016'+'/'+'20160711.zip')  
