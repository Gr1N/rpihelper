# -*- coding: utf-8 -*-

import os

from flask_wtf.csrf import CsrfProtect

from flask import render_template

from rpihelper.config import Flask
from rpihelper.rpihelper import rpihelper
from rpihelper.services import services
from rpihelper.sysmonitor import sysmonitor
from rpihelper.utils import INSTANCE_FOLDER_PATH

__all__ = (
    'create_app',
)


APP_NAME = 'rpihelper'

DEFAULT_BLUEPRINTS = (
    rpihelper,
    services,
    sysmonitor,
)


def create_app(blueprints=None, testing=False):
    if not blueprints:
        blueprints = DEFAULT_BLUEPRINTS

    app = Flask(APP_NAME, instance_path=INSTANCE_FOLDER_PATH, instance_relative_config=True)
    configure_app(app)
    configure_blueprints(app, blueprints)
    configure_extensions(app)
    configure_logging(app)
    configure_template_filters(app)
    configure_hook(app)
    configure_error_handlers(app)

    return app


def configure_app(app):
    config_file = os.environ.get(
        'FLASK_CONFIG_FILE',
        '%s/config_local.yaml' % app.config['PROJECT_ROOT']
    )
    app.config.from_yaml(config_file)


def configure_extensions(app):
    csrf = CsrfProtect()
    csrf.init_app(app)


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
