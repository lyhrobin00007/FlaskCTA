# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 14:05:58 2016

@author: 024536
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import Required, Length, Email, Regexp


class RunForm(FlaskForm):
    name = StringField('Who is ready to run?', validators=[Required()])
    submit = SubmitField('Submit')
    
    
class UploadForm(FlaskForm):
    name = StringField('Upload .py strategy', validators=[Required()])
    submit = SubmitField('Submit')
    
