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
from .forms import RunForm, UploadForm
from .. import db, mongo
from ..models import Permission, Role, User, Post, Comment
from ..decorators import admin_required, permission_required
from .testBacktesting import ctaTest


@ctaAlgo.route('/ctaRun', methods=['GET', 'POST'])
@login_required
def ctaRun():
    form = RunForm()
    if form.validate_on_submit():
        d = ctaTest()
        return jsonify(d)
    form.name.data = current_user.name
    return render_template('ctaAlgo/ctaShow.html', form=form)

    
@ctaAlgo.route('/uploadStrategy', methods=['GET', 'POST'])
@login_required
def uploadStrategy():
    form = UploadForm()
    if form.validate_on_submit():
        d = ctaTest()
        return jsonify(d)
    form.name.data = current_user.name
    return render_template('ctaAlgo/uploadStrategy.html', form=form)
    
    
@ctaAlgo.route('/manageStrategy', methods=['GET', 'POST'])
@login_required
def manageStrategy():
    form = UploadForm()
    if form.validate_on_submit():
        d = ctaTest()
        return jsonify(d)
    form.name.data = current_user.name
    return render_template('ctaAlgo/manageStrategy.html', form=form)