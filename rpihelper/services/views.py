# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

from rpihelper.services.logic import get_services

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
        'services': get_services(),
    })
