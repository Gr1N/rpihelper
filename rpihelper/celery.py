# -*- coding: utf-8 -*-

from celery import Celery

from rpihelper import create_app

__all__ = (
    'current_app',
    'celery',
)


def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


current_app = create_app()
celery = make_celery(current_app)
