# -*- coding: utf-8 -*-

import os

from flask.ext.script import Manager

from rpihelper import create_app


app = create_app()
manager = Manager(app)


@manager.command
@manager.option('-l', '--loglevel', help='Celery worker logging level')
def celery_worker(loglevel='INFO'):
    os.system('celery -A rpihelper.transmission.tasks worker -l %s' % loglevel)


@manager.command
@manager.option('-l', '--loglevel', help='Celery beat logging level')
def celery_beat(loglevel='INFO'):
    os.system('celery -A rpihelper.transmission.tasks beat -l %s' % loglevel)


@manager.command
@manager.option('-tm', '--testmodule', help='Provide test module')
def test(testmodule='discover'):
    """Run unit tests."""
    os.environ['FLASK_ENV'] = 'testing'
    os.system('python -m unittest %s' % testmodule)


if __name__ == '__main__':
    manager.run()
