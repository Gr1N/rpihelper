# -*- coding: utf-8 -*-

import transmissionrpc

from rpihelper.celery import current_app

__all__ = (
    'transmissionrpc_client',
    'transmissionrpc_add_torrent',
)


def transmissionrpc_client():
    try:
        return transmissionrpc.Client(
            address=current_app.config['TRANSMISSION_ADDRESS'],
            port=current_app.config['TRANSMISSION_PORT'],
            timeout=current_app.config['TRANSMISSION_TIMEOUT']
        )
    except transmissionrpc.error.TransmissionError as e:
        current_app.logger.error(e)
        return None


def transmissionrpc_add_torrent(tc, file_url):
    try:
        tc.add_torrent(
            file_url,
            timeout=current_app.config['TRANSMISSION_TIMEOUT']
        )
        return True
    except transmissionrpc.error.TransmissionError as e:
        current_app.logger.error(e)
        return False
