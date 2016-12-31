# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 14:05:58 2016

@author: 024536
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField, FileAllowed
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import Required, Length, Email, Regexp


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
    szMarket = SelectField('szMarket', validators=[Required()],
        choices=[('SZ','SZ'),
                 ('SH','SH'),
                 ('QH','QH'),
                 ('CF','CF'),
                 ('SHF','SHF'),
                 ('CZC','CZC'),
                 ('DCE','DCE')])
    dataType = SelectField('dataType', validators=[Required()],
        choices=[('FutureAB','FutureAB'),
                 ('Future','Future'),
                 ('TickAB','TickAB'),
                 ('Tick','Tick')])
    submit = SubmitField('Submit')    
    

