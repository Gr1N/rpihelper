# -*- coding: utf-8 -*-

from flask import current_app

__all__ = (
    'get_services',
)


def get_services():
    return current_app.config.get('SERVICES', [])
