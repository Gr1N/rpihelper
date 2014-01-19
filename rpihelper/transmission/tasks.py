# -*- coding: utf-8 -*-

from tempfile import NamedTemporaryFile

from rpihelper import create_app
from rpihelper.dropboxclient.logic import Client as DropBoxClient
from rpihelper.transmission.logic import (
    transmissionrpc_client, transmissionrpc_add_torrent,
)

__all__ = (
    'check_torrent_files',
)


def check_torrent_files():
    tc = transmissionrpc_client()
    if not tc:
        current_app.logger.info('No connetion to remote transmission, stop task.')
        return

    dbc = DropBoxClient()
    for f in dbc.folder(current_app.config['TRANSMISSION_DROPBOX_TORRENTS_FOLDER']):
        with NamedTemporaryFile() as tf:
            tf.write(dbc.file(f))
            success = transmissionrpc_add_torrent(tc, 'file://%s' % tf.name)

        if success:
            dbc.rm_file(f)
            current_app.logger.info('Successfully added torrent "%s".' % f)
        else:
            current_app.logger.info('Torrent "%s" not added, skip it.' % f)


current_app = create_app()
