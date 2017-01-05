# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 14:04:43 2016

@author: 024536
"""

from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response, jsonify
from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries
from . import ctaAlgo
from .forms import RunForm, UploadForm, StrategyForm, ManageDataForm, \
    TDB_CodeTableForm, TDB_TickDataForm, \
    TDB_CodeTable, TDB_FutureAB, TDB_TickAB, statDataTable
from .. import db, tickmongo, tdbapi
from ..models import Permission, Role, User, Post, Comment
from ..decorators import admin_required, permission_required
from .ctaAlgoBacktesting import ctaBacktestingRun
import os
import time
from datetime import datetime, timedelta
import pymongo
from threading import Thread


@ctaAlgo.route('/ctaRun', methods=['GET', 'POST'])
@login_required
def ctaRun():
    form = RunForm()
    if form.validate_on_submit():
        d = ctaBacktestingRun()
        return jsonify(d)
    form.name.data = current_user.name
    return render_template('ctaAlgo/ctaShow.html', form=form)

    
@ctaAlgo.route('/uploadStrategy', methods=['GET', 'POST'])
@login_required
def uploadStrategy():
    form = UploadForm()
    if form.validate_on_submit():
        filename = form.uploadFile.data.filename
        print filename
        strategyPath,strategyList = getStrategyDict(current_user.username)
        if filename in strategyList:
            flash('strategy is all ready existed!')
        else:
            form.uploadFile.data.save(os.path.join(strategyPath,filename))
            flash('strategy is all ready upload!')
    return render_template('ctaAlgo/uploadStrategy.html', form=form)
    
    
@ctaAlgo.route('/showStrategy', methods=['GET', 'POST'])
@login_required
def showStrategy():
    strategyPath,tableList = getStrategyDict(current_user.username)    
    form = StrategyForm()
    form.strategyName.choices = [(i,i) for i in tableList] 
    if form.validate_on_submit():
        d = ctaBacktestingRun(current_user.username, form.strategyName.data)
        return jsonify(d)
    return render_template('ctaAlgo/showStrategy.html', form=form)
    
    
@ctaAlgo.route('/manageStrategy', methods=['GET', 'POST'])
@login_required
def manageStrategy():
    strategyPath,tableList = getStrategyDict(current_user.username)  
    form = StrategyForm()
    form.strategyName.choices = [(i,i) for i in tableList] 
    if form.validate_on_submit():
        d = ctaBacktestingRun(current_user.username, form.strategyName.data)
        return jsonify(d)
    return render_template('ctaAlgo/manageStrategy.html', form=form)

    
@ctaAlgo.route('/manageData', methods=['GET', 'POST'])
@login_required
def manageData():
    form = ManageDataForm()
    if form.validate_on_submit():
        chCode = str(form.chCode.data)
        dataType = str(form.dataType.data)
        begDate = str(form.begDate.data)
        endDate = str(form.endDate.data)
        if len(chCode.split('.'))==2 and chCode.split('.')[1]=="CF":
            szPort = "20004"
        else:
            szPort = "20003"
        pSetting = {
            'szIP':"172.22.137.140",
            'szPort':szPort,
            'szUser':"liyonghan",
            'szPassword':"liyo1234",
            'nTimeOutVal':10,
            'nRetryCount':10,
            'nRetryGap':10
        }
        mtdbapi = tdbapi()
        TDB_Open_Dict = mtdbapi.TDB_Open(pSetting)
        mtdbapi.TDB_Close()
        if TDB_Open_Dict['nMarkets'] == 0:
            flash(TDB_Open_Dict['szInfo'])
        else:
            app = current_app._get_current_object()
            thr = Thread(target=load_async_data, args=[app,pSetting,chCode,dataType,begDate,endDate])
            thr.start()
            
        flash('Loading data.')
        return render_template('ctaAlgo/manageData.html', form=form)
    return render_template('ctaAlgo/manageData.html', form=form)

    
@ctaAlgo.route('/tickData', methods=['GET', 'POST'])
@login_required
def TDB_TickDataView():
    form = TDB_TickDataForm()
    if form.validate_on_submit():
        chCode = str(form.chCode.data)
        dataType = str(form.dataType.data)
        strDate = str(form.strDate.data)
        if len(chCode.split('.'))==2 and chCode.split('.')[1]=="CF":
            szPort = "20004"
        else:
            szPort = "20003"
        pSetting = {
            'szIP':"172.22.137.140",
            'szPort':szPort,
            'szUser':"liyonghan",
            'szPassword':"liyo1234",
            'nTimeOutVal':10,
            'nRetryCount':10,
            'nRetryGap':10
        }
        mtdbapi = tdbapi()
        TDB_Open_Dict = mtdbapi.TDB_Open(pSetting)
        if TDB_Open_Dict['nMarkets'] == 0:
            dataTable = TDB_Open_Dict['szInfo']
#            flash(TDB_Open_Dict['szInfo'])
        else:
            #证券万得代码(AG1312.SHF)
            #开始日期（交易日）,为0则从当天，例如20130101
            #结束日期（交易日），小于等于0则和nBeginDate相同
            #开始时间：若<=0则从头，格式：（HHMMSSmmm）例如94500000 表示 9点45分00秒000毫秒
            #结束时间：若<=0则至最后
            #自动补齐标志:( 0：不自动补齐，1:自动补齐）
            req = {"chCode":chCode,
                   "nBeginDate":int(strDate.replace('-','')),
                   "nEndDate":int(strDate.replace('-','')),
                   "nBeginTime":0,
                   "nEndTime":0}
            if dataType in ['FutureAB', 'Future']:
                req['nAutoComplete'] = 0
                data,flag = mtdbapi.TDB_GetFutureAB(req)
                dataTable = TDB_FutureAB(data)
            else:
                data,flag = mtdbapi.TDB_GetTickAB(req)
                dataTable = TDB_TickAB(data)
            dataTable = dataTable
        mtdbapi.TDB_Close()
        return jsonify(dataTable=dataTable,updateTime="UpdateTime: "+time.asctime())
    return render_template('ctaAlgo/TDB_Req_Templete.html', form=form)    
    

@ctaAlgo.route('/codeTable', methods=['GET', 'POST'])
@login_required
def TDB_CodeTableView():
    form = TDB_CodeTableForm()
    if form.validate_on_submit():
        szMarket = str(form.szMarket.data)
        if szMarket == "CF":
            szPort = "20004"
        else:
            szPort = "20003"        
        pSetting = {
            'szIP':"172.22.137.140",
            'szPort':szPort,
            'szUser':"liyonghan",
            'szPassword':"liyo1234",
            'nTimeOutVal':10,
            'nRetryCount':10,
            'nRetryGap':10
        }
        mtdbapi = tdbapi()
        TDB_Open_Dict = mtdbapi.TDB_Open(pSetting)
        if TDB_Open_Dict['nMarkets'] == 0:
            codeTable = TDB_Open_Dict['szInfo']
#            flash(TDB_Open_Dict['szInfo'])
        else:
            codeTable,flagcodeTable = mtdbapi.TDB_GetCodeTable(szMarket)
            codeTable = TDB_CodeTable(codeTable)
        mtdbapi.TDB_Close()
        return jsonify(dataTable=codeTable,updateTime="UpdateTime: "+time.asctime())
    return render_template('ctaAlgo/TDB_Req_Templete.html', form=form)
    
    
@ctaAlgo.route('/statData')
@login_required
def statData():
    statDatas = []
    tmpdb = tickmongo.db
    symbols = tmpdb.collection_names()
    for symbol in symbols:
        d = {}
        d['symbol'] = symbol
        d['begTime'] = tmpdb[symbol].find().sort("datetime",1).limit(1)[0]['datetime'].isoformat()
        d['endTime'] = tmpdb[symbol].find().sort("datetime",-1).limit(1)[0]['datetime'].isoformat()
        statDatas.append(d)
    statDatas = statDataTable(statDatas)
    return render_template('ctaAlgo/statData.html', statDataTables = statDatas)    
    
     
def getStrategyDict(username):
#    strategyPath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"\\strategy\\")
    strategyPath = 'D:\\Code\\github\\FlaskCTA\\app\\ctaAlgo\\strategy'
    strategyPath = os.path.join(strategyPath, username)
    if os.path.exists(strategyPath):
        strategyList = [i.split('.')[0] for i in os.listdir(strategyPath) if i[0]!="_" and i[-2:]=='py']
    else:
        os.mkdir(strategyPath)
        with open(os.path.join(strategyPath,"__init__.py"),'w'):
            pass
        strategyList = []
    return strategyPath, strategyList


def load_async_data(app,pSetting,chCode,dataType,begDate,endDate):
    with app.app_context():
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
            
    #    dbName = 'VnTrader_Tick_Db'
    #    host = 'localhost'
    #    port = 27017
    #    client = pymongo.MongoClient(host, port, connectTimeoutMS=3600)
    #    dbName = 'VnTrader_Tick_Db'
        symbol = chCode.split('.')[0]
    #    database = client[dbName]
        database = tickmongo.db
        collection = database[symbol]
        if symbol not in database.collection_names():
            collection.create_index([('datetime', pymongo.ASCENDING)], unique=True)
        
        for i in range((endDate-begDate).days+1):
            tmpDate = begDate + timedelta(i)
            req["nBeginDate"] = int(tmpDate.isoformat().replace('-',''))
            req["nEndDate"] = int(tmpDate.isoformat().replace('-',''))
            dataList,flag = TDB_GetDataAB(req)
            dataList = tdbapi.cleanDataFutureAB(dataList)
            if len(dataList) == 0:
                continue
            try:
                collection.insert_many(dataList)
            except Exception,e:
                print chCode+" "+tmpDate.isoformat()+" "+str(e)
                for d in dataList:
                    d.pop('_id')
                    flt = {'datetime': d['datetime']}
                    collection.update_one(flt, {'$set':d}, upsert=True)
        mtdbapi.TDB_Close()
        
        