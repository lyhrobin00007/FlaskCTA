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
from .forms import RunForm, UploadForm, StrategyForm, ManageDataForm
from .. import db, mongo, tdbapi
from ..models import Permission, Role, User, Post, Comment
from ..decorators import admin_required, permission_required
from .ctaAlgoBacktesting import ctaBacktestingRun
import os

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
        pSetting = {
            'szIP':"172.22.137.140",
            'szPort':"20003",
            'szUser':"liyonghan",
            'szPassword':"liyo1234",
            'nTimeOutVal':10,
            'nRetryCount':10,
            'nRetryGap':10
        }
        mtdbapi = tdbapi()
        mtdbapi.TDB_Open(pSetting)
        codeTable,flagcodeTable = mtdbapi.TDB_GetCodeTable("CF")
        mtdbapi.TDB_Close()
        return jsonify(codeTable)
    return render_template('ctaAlgo/manageData.html', form=form)
    
    
@ctaAlgo.route('/statData', methods=['GET', 'POST'])
@login_required
def statData():
    strategyPath,tableList = getStrategyDict(current_user.username)  
    form = StrategyForm()
    form.strategyName.choices = [(i,i) for i in tableList] 
    if form.validate_on_submit():
        d = ctaBacktestingRun(current_user.username, form.strategyName.data)
        return jsonify(d)
    return render_template('ctaAlgo/statData.html', form=form)    
    
     
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
    