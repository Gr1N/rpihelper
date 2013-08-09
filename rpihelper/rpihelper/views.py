# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

__all__ = (
    'rpihelper',
)


rpihelper = Blueprint(
    'rpihelper',
    __name__,
    url_prefix='/',
    template_folder='templates',
    static_folder='static'
)


@rpihelper.route('/', methods=('GET',))
def index():
    return render_template('rpihelper/index.html')
