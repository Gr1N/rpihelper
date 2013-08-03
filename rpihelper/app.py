# -*- coding: utf-8 -*-

import os

from flask import Flask, render_template

from rpihelper.config import DefaultConfig, TestConfig
from rpihelper.rpihelper import rpihelper
from rpihelper.sysmonitor import sysmonitor
from rpihelper.utils import INSTANCE_FOLDER_PATH

__all__ = (
    'create_app',
)


DEFAULT_BLUEPRINTS = (
    rpihelper,
    sysmonitor,
)


def create_app(app_name=None, blueprints=None, testing=False):
    if not app_name:
        app_name = DefaultConfig.PROJECT

    if not blueprints:
        blueprints = DEFAULT_BLUEPRINTS

    app = Flask(app_name, instance_path=INSTANCE_FOLDER_PATH, instance_relative_config=True)
    configure_app(app, TestConfig if testing else DefaultConfig)
    configure_blueprints(app, blueprints)
    configure_extensions(app)
    configure_logging(app)
    configure_template_filters(app)
    configure_hook(app)
    configure_error_handlers(app)

    return app


def configure_app(app, config):
    # http://flask.pocoo.org/docs/api/#configuration
    app.config.from_object(config)

    # http://flask.pocoo.org/docs/config/#instance-folders
    # app.config.from_pyfile('production.cfg', silent=True)

    # Use instance folder instead of env variables to make deployment easier.
    #app.config.from_envvar('%s_APP_CONFIG' % DefaultConfig.PROJECT.upper(), silent=True)


def configure_extensions(app):
    pass


def configure_blueprints(app, blueprints):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def configure_template_filters(app):

    @app.template_filter()
    def pretty_date(value):
        return pretty_date(value)

    @app.template_filter()
    def format_date(value, format='%Y-%m-%d'):
        return value.strftime(format)


def configure_logging(app):
    if app.debug or app.testing:
        # Skip debug and test mode. Just check standard output.
        return

    import logging

    # Set info level on logger, which might be overwritten by handers.
    # Suppress DEBUG messages.
    app.logger.setLevel(logging.INFO)

    info_log = os.path.join(app.config['LOG_FOLDER'], 'info.log')
    info_file_handler = logging.handlers.RotatingFileHandler(info_log, maxBytes=100000, backupCount=10)
    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')
    )
    app.logger.addHandler(info_file_handler)

    # Testing
    #app.logger.info('testing info.')
    #app.logger.warn('testing warn.')
    #app.logger.error('testing error.')


def configure_hook(app):
    @app.before_request
    def before_request():
        pass


def configure_error_handlers(app):

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template('errors/500.html'), 500
