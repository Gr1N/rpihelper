# -*- coding: utf-8 -*-

from subprocess import getoutput
import re

from flask import current_app

__all__ = (
    'SystemctlCommands',
    'SystemctlStatuses',

    'get_services',
    'get_services_with_status',

    'systemctl_ssr_command',
    'systemctl_status_command',
)


class SystemctlCommands(object):
    START = 'start'
    STOP = 'stop'
    RESTART = 'restart'


class SystemctlStatuses(object):
    ACTIVE = 'active'
    INACTIVE = 'inactive'

    UNKNOWN = 'unknown'


def get_services():
    return current_app.config.get('SERVICES', ())


def get_services_with_status():
    services = get_services()

    for service in services:
        service['status'] = systemctl_status_command(service['name'])

    return services


def systemctl_ssr_command(command, service, with_sudo=True):
    """
    Execute `systemctl start/stop/restart <service_name>`.
    If output returned we think that this is error.

    NOTE: if you use this function `with_sudo`, you shoud pass to
    your `sudoers` config, something like this:
        %http ALL=(ALL) NOPASSWD: ALL

    TODO: pass `with_sudo` parameter via app config.
    """
    cmd = 'systemctl %s %s' % (command, service)
    cmd = 'sudo %s' % cmd if with_sudo else cmd

    output = getoutput(cmd)
    return bool(output)


def systemctl_status_command(service, with_sudo=True):
    """
    Check service status with `systemctl status <service_name>`.

    NOTE: if you use this function `with_sudo`, you shoud pass to
    your `sudoers` config, something like this:
        %http ALL=(ALL) NOPASSWD: ALL

    TODO: pass `with_sudo` parameter via app config.
    """
    cmd = 'systemctl status %s' % service
    cmd = 'sudo %s' % cmd if with_sudo else cmd

    output = getoutput(cmd)
    match = re.search(r'(?<=Active: )\w+', output)

    if not match:
        return SystemctlStatuses.UNKNOWN

    return match.group(0)
