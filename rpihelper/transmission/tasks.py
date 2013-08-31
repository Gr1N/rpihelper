# -*- coding: utf-8 -*-

from rpihelper.celery import current_app, celery
from rpihelper.dropboxclient.logic import Client as DropBoxClient
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

    dbc = DropBoxClient()
    for f in dbc.folder(current_app.config['TRANSMISSION_DROPBOX_TORRENTS_FOLDER']):
        file_url = dbc.file_url(f)
        success = transmissionrpc_add_torrent(tc, file_url)
        if success:
            dbc.rm_file(f)
            current_app.logger.info('Successfully added torrent "%s".' % file_url)
        else:
            current_app.logger.info('Torrent "%s" not added, skip it.' % file_url)
