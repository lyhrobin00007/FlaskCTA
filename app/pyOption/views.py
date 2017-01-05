from flask import render_template, redirect, request, url_for, flash, jsonify, session
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import pyOption
from .. import db
from ..models import User
from ..email import send_email
from .forms import pyOptionForm, pyOptionHomeForm, BsmForm, BullSpreadForm, OptionMCSForm1, OptionMCSForm2, OptionMCSForm3, ItemTable
from .bsm_option_class import EuropeanOptionClass, BullSpreadClass
from .mcs_option_class import mcsOptionClass, BullSpreadPathNClass, DoubleNoTouchClass, OutOfRangeRateClass, DownAndOutAlternativeClass, ModerateOptionClass

import time

@pyOption.route('/European', methods=['GET', 'POST'])
@login_required
def European():
    form = BsmForm()
    tableResult = 'Calculation Result'
    description = EuropeanOptionClass.__doc__.split('\n')
    if form.validate_on_submit() and request.method == "POST":
        S0 = form.S0.data
        K  = form.K.data
        T  = form.T.data
        r  = form.r.data
        q  = form.q.data
        sigma = form.sigma.data
        optionType = form.optionType.data
        try:
            option = EuropeanOptionClass(S0, K, T, r, sigma, optionType, q)
            result = option.dictResult()
            items = [dict(name='value', valuation=result['value'], ratio=result['valueRatio']),
                     dict(name='delta', valuation=result['delta'], ratio=result['deltaRatio']),
                     dict(name='theta', valuation=result['theta'], ratio=result['thetaRatio']),
                     dict(name='gamma', valuation=result['gamma'], ratio=result['gammaRatio']),
                     dict(name='vega' , valuation=result['vega'] , ratio=result['vegaRatio'])]  
            tableResult = ItemTable(items).__html__()
        except Exception,e:
            flash(str(e))
        return jsonify(tableResult=tableResult)
#    return render_template("pyOption/baseOption.html", name='European', form=form, tableResult=tableResult, description=description)
    return render_template("pyOption/pyOptionHome.html", name='European', form=form, tableResult=tableResult, description=description)  
    
@pyOption.route('/BullSpread', methods=['GET', 'POST'])
@login_required
def BullSpread():
    form = BullSpreadForm()
    tableResult = 'Calculation Result'
    description = BullSpreadClass.__doc__.split('\n')
    if form.validate_on_submit():
        S0 = form.S0.data
        K1  = form.K1.data
        K2  = form.K2.data
        T  = form.T.data
        r  = form.r.data
        q  = form.q.data
        sigma = form.sigma.data
        optionType = form.optionType.data
        try:
            option = BullSpreadClass(S0, K1, K2, T, r, sigma, optionType, q)
            result = option.dictResult()
            items = [dict(name='value', valuation=result['value'], ratio=result['valueRatio']),
                     dict(name='delta', valuation=result['delta'], ratio=result['deltaRatio']),
                     dict(name='theta', valuation=result['theta'], ratio=result['thetaRatio']),
                     dict(name='gamma', valuation=result['gamma'], ratio=result['gammaRatio']),
                     dict(name='vega' , valuation=result['vega'] , ratio=result['vegaRatio'])]  
            tableResult = ItemTable(items)
        except Exception,e:
            flash(str(e))
    return render_template("pyOption/baseOption.html", name='Bull Spread', form=form, tableResult=tableResult, description=description)

    
@pyOption.route('/OptionMCS1', methods=['GET', 'POST'])
@login_required
def OptionMCS1():
    form = OptionMCSForm1()
    tableResult = 'Calculation Result'
    description = mcsOptionClass.__doc__.split('\n')
    if form.validate_on_submit():
        S0 = form.S0.data
        K1 = form.K1.data
        K2 = form.K2.data
        T  = form.T.data
        r  = form.r.data
        q  = form.q.data
        sigma = form.sigma.data
        optionType = form.optionType.data
        optionStyle = form.optionStyle.data
        N  = form.N.data
        I  = form.I.data 
        M  = form.M.data
        seedNum = form.seedNum.data
        
        try:
            if optionStyle == 'BullSpreadPathN':
                option = BullSpreadPathNClass(S0,K1,K2,T,r,q,sigma,N,optionType,I,M,seedNum)
            result = option.dictResult()
            items = [dict(name='value', valuation=result['value'], ratio=result['valueRatio']),
                     dict(name='delta', valuation=result['delta'], ratio=result['deltaRatio']),
                     dict(name='theta', valuation=result['theta'], ratio=result['thetaRatio']),
                     dict(name='gamma', valuation=result['gamma'], ratio=result['gammaRatio']),
                     dict(name='vega' , valuation=result['vega'] , ratio=result['vegaRatio'])]  
            tableResult = ItemTable(items)
        except Exception,e:
            flash(str(e))
    else:
        form.I.data = 10000
        form.M.data = 100
        form.seedNum.data = 2000
    return render_template("pyOption/baseOption.html", name='Option MCS 1', form=form, tableResult=tableResult, description=description)  

@pyOption.route('/OptionMCS2', methods=['GET', 'POST'])
@login_required
def OptionMCS2():
    form = OptionMCSForm2()
    tableResult = 'Calculation Result'
    description = mcsOptionClass.__doc__.split('\n')
    if form.validate_on_submit():
        S0 = form.S0.data
        K1 = form.K1.data
        K2 = form.K2.data
        T  = form.T.data
        r  = form.r.data
        q  = form.q.data
        sigma = form.sigma.data
        optionType = form.optionType.data
        optionStyle = form.optionStyle.data
        Rp = form.Rp.data
        I  = form.I.data 
        M  = form.M.data
        seedNum = form.seedNum.data
        
        try:
            if optionStyle == 'DoubleNoTouch':
                option = DoubleNoTouchClass(S0,K1,K2,T,r,q,sigma,Rp,optionType,I,M,seedNum)
            elif optionStyle == 'OutOfRangeRate':
                option = OutOfRangeRateClass(S0,K1,K2,T,r,q,sigma,Rp,optionType,I,M,seedNum)
            result = option.dictResult()
            items = [dict(name='value', valuation=result['value'], ratio=result['valueRatio']),
                     dict(name='delta', valuation=result['delta'], ratio=result['deltaRatio']),
                     dict(name='theta', valuation=result['theta'], ratio=result['thetaRatio']),
                     dict(name='gamma', valuation=result['gamma'], ratio=result['gammaRatio']),
                     dict(name='vega' , valuation=result['vega'] , ratio=result['vegaRatio'])]  
            tableResult = ItemTable(items)
        except Exception,e:
            flash(str(e))
    else:
        form.I.data = 10000
        form.M.data = 100
        form.seedNum.data = 2000
    return render_template("pyOption/baseOption.html", name='Option MCS 2', form=form, tableResult=tableResult, description=description)  

@pyOption.route('/OptionMCS3', methods=['GET', 'POST'])
@login_required
def OptionMCS3():
    form = OptionMCSForm3()
    tableResult = 'Calculation Result'
    description = mcsOptionClass.__doc__.split('\n')
    if form.validate_on_submit():
        S0 = form.S0.data
        K  = form.K.data
        T  = form.T.data
        r  = form.r.data
        q  = form.q.data
        sigma = form.sigma.data
        optionType = form.optionType.data
        optionStyle = form.optionStyle.data
        Rp = form.Rp.data
        I  = form.I.data 
        M  = form.M.data
        seedNum = form.seedNum.data
        
        try:
            if optionStyle == 'DownAndOutAlternative':
                option = DownAndOutAlternativeClass(S0,K,T,r,q,sigma,Rp,optionType,I,M,seedNum)
            elif optionStyle == 'ModerateOption':
                option = ModerateOptionClass(S0,K,T,r,q,sigma,Rp,optionType,I,M,seedNum)
                
            result = option.dictResult()
            items = [dict(name='value', valuation=result['value'], ratio=result['valueRatio']),
                     dict(name='delta', valuation=result['delta'], ratio=result['deltaRatio']),
                     dict(name='theta', valuation=result['theta'], ratio=result['thetaRatio']),
                     dict(name='gamma', valuation=result['gamma'], ratio=result['gammaRatio']),
                     dict(name='vega' , valuation=result['vega'] , ratio=result['vegaRatio'])]  
            tableResult = ItemTable(items)
        except Exception,e:
            flash(str(e))
    else:
        form.I.data = 10000
        form.M.data = 100
        form.seedNum.data = 2000
    return render_template("pyOption/baseOption.html", name='Option MCS 3', form=form, tableResult=tableResult, description=description)  

    
@pyOption.route('/pyOptionIndex', methods=['GET', 'POST'])
@login_required
def pyOptionIndex():
    form = pyOptionForm()
    tableResult = 'Calculation Result'
    description = EuropeanOptionClass.__doc__.split('\n')
    inputs = ['S0','K','K1','K2','T','r','q','sigma','N','Rp','I','M','seedNum']
    inputsHide = ['hideS0','hideK','hideK1','hideK2','hideT','hider','hideq',
                  'hidesigma','hideN','hideRp','hideI','hideM','hideSeed']
    if form.validate_on_submit():
        S0 = form.S0.data
        K  = form.K.data
        T  = form.T.data
        r  = form.r.data
        q  = form.q.data
        sigma = form.sigma.data
        optionType = form.optionType.data
        try:
            option = EuropeanOptionClass(S0, K, T, r, sigma, optionType, q)
            result = option.dictResult()
            items = [dict(name='value', valuation=result['value'], ratio=result['valueRatio']),
                     dict(name='delta', valuation=result['delta'], ratio=result['deltaRatio']),
                     dict(name='theta', valuation=result['theta'], ratio=result['thetaRatio']),
                     dict(name='gamma', valuation=result['gamma'], ratio=result['gammaRatio']),
                     dict(name='vega' , valuation=result['vega'] , ratio=result['vegaRatio'])]  
            tableResult = ItemTable(items)
        except Exception,e:
            flash(str(e))
    return render_template("pyOption/pyOptionIndex.html", name='Option Index', 
                           form=form, tableResult=tableResult, description=description, 
                           inputs=inputs, inputsHide=inputsHide)

    
@pyOption.route('/_pyOptionIndex', methods=['GET', 'POST'])
@login_required
def _pyOptionIndex():
#    count = request.data.get('count', 0, type=int)
    dictData = request.json
    S0 = float(dictData.setdefault('S0', 0))
    K = float(dictData.setdefault('K', 0))
    K1 = float(dictData.setdefault('K1', 0))
    K2 = float(dictData.setdefault('K2', 0))
    T = float(dictData.setdefault('T', 0))
    r = float(dictData.setdefault('r', 0))
    q = float(dictData.setdefault('q', 0))
    sigma = float(dictData.setdefault('sigma', 0))
    N = int(dictData.setdefault('N', 0))
    Rp = float(dictData.setdefault('Rp', 0))
    I = int(dictData.setdefault('I', 0))
    M = int(dictData.setdefault('M', 0))
    seedNum = int(dictData.setdefault('seedNum', 0))
    optionType = dictData.setdefault('optionType', 'call') 
    optionStyle = dictData.setdefault('optionStyle', 'BullSpreadPathN') 
    
    try:
        if optionStyle == 'European':
            option = EuropeanOptionClass(S0, K, T, r, sigma, optionType, q)
        elif optionStyle == 'BullSpread':
            option = BullSpreadClass(S0, K1, K2, T, r, sigma, optionType, q)
        elif optionStyle == 'BullSpreadPathN':
            option = BullSpreadPathNClass(S0,K1,K2,T,r,q,sigma,N,optionType,I,M,seedNum)
        elif optionStyle == 'DoubleNoTouch':
            option = DoubleNoTouchClass(S0,K1,K2,T,r,q,sigma,Rp,optionType,I,M,seedNum)
        elif optionStyle == 'OutOfRangeRate':
            option = OutOfRangeRateClass(S0,K1,K2,T,r,q,sigma,Rp,optionType,I,M,seedNum)
        elif optionStyle == 'DownAndOutAlternative':
            option = DownAndOutAlternativeClass(S0,K,T,r,q,sigma,Rp,optionType,I,M,seedNum)
        elif optionStyle == 'ModerateOption':
            option = ModerateOptionClass(S0,K,T,r,q,sigma,Rp,optionType,I,M,seedNum)
            
        result = option.dictResult()
        items = [dict(name='value', valuation=result['value'], ratio=result['valueRatio']),
                 dict(name='delta', valuation=result['delta'], ratio=result['deltaRatio']),
                 dict(name='theta', valuation=result['theta'], ratio=result['thetaRatio']),
                 dict(name='gamma', valuation=result['gamma'], ratio=result['gammaRatio']),
                 dict(name='vega' , valuation=result['vega'] , ratio=result['vegaRatio'])]  
        tableResult = ItemTable(items).__html__()
    except Exception,e:
        tableResult = "No Result! <br/> Error: "+str(e)+"<br/>"
    tableResult = tableResult +"Update Time: "+time.asctime()    
#    strData = request.data
    return jsonify(updateTime=time.asctime(), tableResult=tableResult )


@pyOption.route('/pyOptionHome', methods=['GET', 'POST'])
@login_required
def pyOptionHome():
    form = pyOptionHomeForm()
    tableResult = 'Calculation Result'
    begTime = time.clock()
    
    if request.method == "POST" and form.is_submitted():
        S0 = form.S0.data
        K  = form.K.data
        K1 = form.K1.data
        K2 = form.K2.data
        T  = form.T.data
        r  = form.r.data
        q  = form.q.data
        sigma = form.sigma.data
        N  = form.N.data
        Rp = form.Rp.data
        I  = form.I.data
        M  = form.M.data
        seedNum = form.seedNum.data
        optionType = form.optionType.data
        optionStyle = form.optionStyle.data
        try:
            if optionStyle == 'European':
                option = EuropeanOptionClass(S0, K, T, r, sigma, optionType, q)
            elif optionStyle == 'BullSpread':
                option = BullSpreadClass(S0, K1, K2, T, r, sigma, optionType, q)
            elif optionStyle == 'BullSpreadPathN':
                option = BullSpreadPathNClass(S0,K1,K2,T,r,q,sigma,N,optionType,I,M,seedNum)
            elif optionStyle == 'DoubleNoTouch':
                option = DoubleNoTouchClass(S0,K1,K2,T,r,q,sigma,Rp,optionType,I,M,seedNum)
            elif optionStyle == 'OutOfRangeRate':
                option = OutOfRangeRateClass(S0,K1,K2,T,r,q,sigma,Rp,optionType,I,M,seedNum)
            elif optionStyle == 'DownAndOutAlternative':
                option = DownAndOutAlternativeClass(S0,K,T,r,q,sigma,Rp,optionType,I,M,seedNum)
            elif optionStyle == 'ModerateOption':
                option = ModerateOptionClass(S0,K,T,r,q,sigma,Rp,optionType,I,M,seedNum)
                
            result = option.dictResult()
            items = [dict(name='value', valuation=result['value'], ratio=result['valueRatio']),
                     dict(name='delta', valuation=result['delta'], ratio=result['deltaRatio']),
                     dict(name='theta', valuation=result['theta'], ratio=result['thetaRatio']),
                     dict(name='gamma', valuation=result['gamma'], ratio=result['gammaRatio']),
                     dict(name='vega' , valuation=result['vega'] , ratio=result['vegaRatio'])]
            tableResult = ItemTable(items).__html__()
        except Exception,e:
            tableResult = "No Result! <br/> Error: "+str(e)+"<br/>"
        tableResult = tableResult+"Run Time:  "+ str(time.clock()-begTime)[0:6] +" s <br/>Update Time:  "+time.asctime()
        return jsonify(tableResult=tableResult )
    return render_template("pyOption/pyOptionHome.html", name='Option Home', 
                           form=form, tableResult=tableResult )

    