# -*- coding: utf-8 -*-

from functools import wraps

from dropbox import rest

from flask import current_app

from rpihelper.dropboxclient.exceptions import ApiClientRequired

__all__ = (
    'command',
)


def command(exception_return=None):
    """
    A decorator for handling authentication and exceptions.
    """
    def decorate(func):

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self.api_client:
                current_app.logger.error('API client required.')
                raise ApiClientRequired

            try:
                return func(self, *args)
            except (rest.RESTSocketError, rest.ErrorResponse) as e:
                current_app.logger.error(e)
                return exception_return

        return wrapper

    return decorate
