# -*- coding: utf-8 -*-

from flask import Blueprint, render_template


rpihelper = Blueprint('rpihelper', __name__)


@rpihelper.route('/')
def index():
    return render_template('index.html')
