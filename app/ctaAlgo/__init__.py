# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 14:04:10 2016

@author: 024536
"""

from flask import Blueprint

ctaAlgo = Blueprint('ctaAlgo', __name__)

from . import views
