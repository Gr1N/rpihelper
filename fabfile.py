# -*- coding: utf-8 -*-

from datetime import datetime
import os
import time

import yaml

from fabric.api import task, run, cd
from fabric.context_managers import prefix, shell_env
from fabric.contrib.files import exists, upload_template
from fabric.utils import abort

__all__ = (
    'deploy',
    'undeploy',
    'update',

    'schedule_tasks',
)


PROJECT = 'rpihelper'

CONFIG_SHARED = '__shared'
CONFIG_TEMPLATE_DIR = 'templates'

# paths below are relative to project home
VIRTUALENV_DIR = 'app/env'
VIRTUALENV_ACTIVATE = '%s/bin/activate' % VIRTUALENV_DIR
INITIAL_DIRS = (
    'conf/rpihelper',
    'conf/httpd',
    'conf/nginx',
    'conf/supervisord',
    'logs',
)


@task
def deploy(config_file):
    config = load_and_verify_config(config_file)
    if config:
        deploy_project(config)


@task
def undeploy(config_file):
    config = load_and_verify_config(config_file)
    if config:
        undeploy_project(config)


@task
def update(config_file):
    config = load_and_verify_config(config_file)
    if config:
        update_project(config)


@task
def schedule_tasks(config_file):
    config = load_and_verify_config(config_file)
    if config:
        home = config['app']['home']
        with cd(home):
            with prefix('source %s' % VIRTUALENV_ACTIVATE):
                app = config['app']
                with shell_env(FLASK_ENV=app['environment'], FLASK_CONFIG_FILE=app['config']):
                    run('rqscheduletasks')


def load_and_verify_config(config_file):
    with open(config_file, 'r') as stream:
        config = yaml.load(stream)
        project_config = config.get(PROJECT)
        if not project_config:
            abort('No configuration for project "%s" in "%s"' % (PROJECT, config_file))

        home = project_config.get('home')
        if not home:
            abort('Empty "home" for project "%s" in "%s"' % (PROJECT, config_file))

        # dirty but ensures safety for system
        root = config[CONFIG_SHARED]['root']
        assert home.startswith(root)
        assert ' ' not in home

        config['app'] = project_config
        config['PROJECT'] = PROJECT

        config['TIMESTAMP'] = time.mktime(datetime.utcnow().utctimetuple())

        return config


def deploy_project(config):
    home = config['app']['home']
    ensure_environment(home, config)
    deploy_project_package(home, config)
    deploy_configurations(home, config)


def undeploy_project(config):
    home = config['app']['home']
    destroy_environment(home)


def update_project(config):
    home = config['app']['home']
    deploy_configurations(home, config)


def ensure_environment(home, config):
    if not exists(home):
        run('mkdir "%s"' % home)

    ensure_virtualenv(home, config)
    ensure_layout(home)


def destroy_environment(home):
    if exists(home):
        run('rm -rf "%s"' % home)


def ensure_virtualenv(home, config):
    with cd(home):
        if exists(VIRTUALENV_ACTIVATE):
            return

        python = config[CONFIG_SHARED]['PYTHON']
        run('virtualenv "%s" --distribute --python=%s' % (VIRTUALENV_DIR, python))


def ensure_layout(home):
    with cd(home):
        run('mkdir -p "%s"' % '" "'.join(INITIAL_DIRS))


def deploy_project_package(home, config):
    with cd(home):
        with prefix('source %s' % VIRTUALENV_ACTIVATE):
            run('pip install -U %s' % config['app']['pipgit'])


def deploy_configurations(home, config):
    for filename in config[CONFIG_SHARED]['configurations']:
        template = os.path.join(CONFIG_TEMPLATE_DIR, filename)
        if not os.path.exists(template):
            continue

        destination = os.path.join(home, filename)
        upload_template(template, destination, context=config, use_jinja=True)
