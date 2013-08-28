# -*- coding: utf-8 -*-

from functools import wraps

from flask import current_app

__all__ = (
    'systemctl_available',
)


def systemctl_available(return_value=None):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_app.config.get('SERVICES_SYSTEMCTL_AVAILABLE', True):
                return func(*args, **kwargs)
            return return_value

        return wrapper

    return decorator
