# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, jsonify

from rpihelper.services.forms import ServicesForm
from rpihelper.services.logic import get_services, systemctl_ssr_command

__all__ = (
    'ERR_EXECUTE_COMMAND',

    'services',
)


ERR_EXECUTE_COMMAND = 'An error occurred while executing command "%s" for service "%s"'


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
        command = form.command.data
        service = form.service.data

        error = systemctl_ssr_command(command, service)
        if error:
            error = ERR_EXECUTE_COMMAND % (command, service)
            return jsonify(status='error', error=error)

        return jsonify(status='ok')

    return jsonify(status='error', errors=form.errors)
