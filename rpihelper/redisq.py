# -*- coding: utf-8 -*-

from rpihelper import create_app

__all__ = (
    'current_app',
)


current_app = create_app()


def scheduler_run():
    from datetime import datetime

    from rq import use_connection
    from rq_scheduler import Scheduler

    from rpihelper.transmission.tasks import check_torrent_files


    use_connection()
    scheduler = Scheduler(
        current_app.config['RQ_QUEUE_NAME'],
        interval=current_app.config['RQ_SCHEDULER_INTERVAL']
    )

    scheduled_jobs = scheduler.connection.zrange(scheduler.scheduled_jobs_key, 0, -1)
    for job in scheduled_jobs:
        scheduler.connection.delete('rq:job:{0}'.format(job.decode()))
    scheduler.connection.delete(scheduler.scheduled_jobs_key)

    scheduler.schedule(
        scheduled_time=datetime.utcnow(),
        func=check_torrent_files,
        interval=current_app.config['RQ_SCHEDULER_JOB_INTERVAL'],
    )

    scheduler.run()


if __name__ == '__main__':
    scheduler_run()
