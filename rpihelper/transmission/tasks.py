# -*- coding: utf-8 -*-

import os
import os.path

import transmissionrpc

from rpihelper.celery import current_app, celery

__all__ = (
    'check_torrent_files',
)


@celery.task
def check_torrent_files():
    print('check_torrent_files')

    try:
        tc = transmissionrpc.Client(
            address=current_app.config['TRANSMISSION_ADDRESS'],
            port=current_app.config['TRANSMISSION_PORT'],
            timeout=current_app.config['TRANSMISSION_TIMEOUT']
        )
    except transmissionrpc.error.TransmissionError as e:
        # TODO: logging?
        return

    transmission_directory = current_app.config['TRANSMISSION_DROPBOX_DIRECORY']
    for dirpath, diranames, filenames in os.walk(transmission_directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            tc.add_torrent(file_path)  # TODO: try/except
            os.remove(file_path)
