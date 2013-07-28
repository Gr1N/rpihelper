# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

__all__ = (
    'rpihelper',
)


rpihelper = Blueprint(
    'rpihelper',
    __name__,
    template_folder='templates/rpihelper',
    static_folder='static/rpihelper'
)


@rpihelper.route('/', methods=('GET',))
def index():
    return render_template('index.html')
