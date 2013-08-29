# -*- coding: utf-8 -*-

import os
import os.path

from rpihelper.celery import current_app, celery
from rpihelper.transmission.logic import (
    transmissionrpc_client, transmissionrpc_add_torrent,
)

__all__ = (
    'check_torrent_files',
)


@celery.task
def check_torrent_files():
    tc = transmissionrpc_client()
    if not tc:
        current_app.logger.info('No connetion to remote transmission, stop task.')
        return

    walk_directory = current_app.config['TRANSMISSION_DROPBOX_DIRECTORY']
    for dirpath, diranames, filenames in os.walk(walk_directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            success = transmissionrpc_add_torrent(tc, file_path)
            if success:
                os.remove(file_path)
                current_app.logger.info('Successfully added torrent file "%s".' % file_path)
            else:
                current_app.logger.info('Torrent file "%s" not added, skip it.' % file_path)
