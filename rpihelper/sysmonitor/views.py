# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

from rpihelper.sysmonitor.logic import get_system_info

__all__ = (
    'sysmonitor',
)


sysmonitor = Blueprint(
    'sysmonitor',
    __name__,
    url_prefix='/sysmonitor',
    template_folder='templates',
    static_folder='static'
)


@sysmonitor.route('/', methods=('GET',))
def index():
    return render_template('sysmonitor/index.html', **get_system_info())
