# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 14:05:58 2016

@author: 024536
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField, FileAllowed
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import Required, Length, Email, Regexp
from flask_table import Table, Col
from flask_admin.form.widgets import DatePickerWidget


class RunForm(FlaskForm):
    name = StringField('Who is ready to run?', validators=[Required()])
    submit = SubmitField('Submit')    
    
    
class UploadForm(FlaskForm):
    uploadFile = FileField('Upload .py strategy', validators=[FileRequired(),FileAllowed(['py'], 'Python script only!')])
    submit = SubmitField('Submit')
    

class StrategyForm(FlaskForm):
    strategyName = SelectField('Strategy', validators=[Required()])
    submit = SubmitField('Submit')
    

class ManageDataForm(FlaskForm):
    chCode = StringField('chCode', validators=[Required()])
    dataType = SelectField('dataType', validators=[Required()],
        choices=[('FutureAB','FutureAB'),
                 ('Future','Future'),
                 ('TickAB','TickAB'),
                 ('Tick','Tick')])
    begDate = DateField('begDate', validators=[Required()])
    endDate = DateField('endDate', validators=[Required()])
    submit = SubmitField('submit')

    
class TDB_TickDataForm(FlaskForm):
    chCode = StringField('chCode', validators=[Required()])
    dataType = SelectField('dataType', validators=[Required()],
        choices=[('FutureAB','FutureAB'),
                 ('Future','Future'),
                 ('TickAB','TickAB'),
                 ('Tick','Tick')])
    strDate = DateField('strDate', validators=[Required()])
    submit = SubmitField('submit')
    
    
class TDB_CodeTableForm(FlaskForm):
    szMarket = SelectField('szMarket', validators=[Required()],
        choices=[('SZ','SZ'),
                 ('SH','SH'),
                 ('QH','QH'),
                 ('CF','CF'),
                 ('SHF','SHF'),
                 ('CZC','CZC'),
                 ('DCE','DCE')])
    submit = SubmitField('submit')
    
class TDB_CodeTable(Table):
    classes = ['table','table-striped']
    chWindCode = Col('chWindCode')
    chCNName = Col('chCNName')
    chCode = Col('chCode')
#    chENName = Col('chENName')
    chMarket = Col('chMarket')
    nType = Col('nType')

class TDB_FutureAB(Table):
    classes = ['table','table-striped']
    chWindCode = Col('chWindCode')
    nDate = Col("nDate")
    nTime = Col("nTime")
#    iVolume = Col("iVolume")
#    iTurover = Col("iTurover")
    iAccVolume = Col("iAccVolume")
    iAccTurover = Col("iAccTurover")
    nAskPrice1 = Col("nAskPrice1")
    nAskVolume1 = Col("nAskVolume1")
    nBidPrice1 = Col("nBidPrice1")
    nBidVolume1 = Col("nBidVolume1")
    nPosition = Col("nPosition")
#    nHigh = Col("nHigh")
#    nLow = Col("nLow")
#    nOpen = Col("nOpen")
#    nPrice = Col("nPrice")
#    nPrePosition = Col("nPrePosition")
#    nPreClose = Col("nPreClose")
#    nPreSettle = Col("nPreSettle")
#    nSettle = Col("nSettle")
#    nCurDelta = Col("nCurDelta")
#    chTradeFlag = Col("chTradeFlag")             

class TDB_TickAB(Table):
    classes = ['table','table-striped']
    chWindCode = Col('chWindCode')
    nDate = Col("nDate")
    nTime = Col("nTime")
#    iVolume = Col("iVolume")
#    iTurover = Col("iTurover")
    iAccVolume = Col("iAccVolume")
    iAccTurover = Col("iAccTurover")
    nAskPrice1 = Col("nAskPrice1")
    nAskVolume1 = Col("nAskVolume1")
    nBidPrice1 = Col("nBidPrice1")
    nBidVolume1 = Col("nBidVolume1")

class statDataTable(Table):
    classes = ['table','table-striped']
    symbol = Col('symbol')
    begTime = Col("begTime")
    endTime = Col("endTime")
