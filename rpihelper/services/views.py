# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, current_app

__all__ = (
    'services',
)


services = Blueprint(
    'services',
    __name__,
    url_prefix='/services',
    template_folder='templates',
    static_folder='static'
)


@services.route('/', methods=('GET',))
def index():
    return render_template('services/index.html', **{
        'services': current_app.config['SERVICES'],
    })
