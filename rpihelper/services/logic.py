# -*- coding: utf-8 -*-

from subprocess import call

from flask import current_app

__all__ = (
    'SystemctlCommands',

    'get_services',
    'call_command',
)


class SystemctlCommands(object):
    START = 'start'
    STOP = 'stop'
    RESTART = 'restart'


def get_services():
    return current_app.config.get('SERVICES', ())


def call_command(command, service):
    # TODO: docstring, fix code
    call(['sudo', 'systemctl', command, service])
