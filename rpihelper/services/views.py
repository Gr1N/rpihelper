# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, jsonify

from rpihelper.services.forms import ServicesForm
from rpihelper.services.logic import get_services, call_command

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


@services.route('/send_service_command/', methods=('POST',))
def send_service_command():
    form = ServicesForm()

    if form.validate_on_submit():
        call_command(form.command.data, form.service.data)
        return jsonify(status='ok')

    return jsonify(status='error', errors=form.errors)
