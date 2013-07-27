# -*- coding: utf-8 -*-

import os

from rpihelper.utils import make_dir, INSTANCE_FOLDER_PATH

__all__ = (
    'DefaultConfig',
)


class BaseConfig(object):
    PROJECT = 'rpihelper'

    # Get app root path, also can use flask.root_path.
    # ../../config.py
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    DEBUG = False
    TESTING = False

    ADMINS = (
        'grin.minsk@gmail.com'
    )

    # http://flask.pocoo.org/docs/quickstart/#sessions
    SECRET_KEY = 'secret key'

    LOG_FOLDER = os.path.join(INSTANCE_FOLDER_PATH, 'logs')
    make_dir(LOG_FOLDER)


class DefaultConfig(BaseConfig):
    DEBUG = True


class TestConfig(BaseConfig):
    TESTING = True
    CSRF_ENABLED = False
