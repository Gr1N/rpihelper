# -*- coding: utf-8 -*-

import transmissionrpc

from unittest import TestCase
from unittest.mock import patch, MagicMock

from rpihelper.transmission.logic import (
    transmissionrpc_client, transmissionrpc_add_torrent,
)

__all__ = (
    'TransmissionrpcClientLogicTests',
    'TransmissionrpcAddTorrentLogicTests',
)


def raise_exception(*args, **kwargs):
    raise transmissionrpc.error.TransmissionError


class TransmissionrpcClientLogicTests(TestCase):
    @patch('rpihelper.transmission.logic.transmissionrpc.Client')
    def test_ok(self, mock_client):
        tc = transmissionrpc_client()

        mock_client.assert_called_once()
        self.assertTrue(isinstance(tc, MagicMock))

    @patch('rpihelper.transmission.logic.transmissionrpc.Client', new=raise_exception)
    def test_transmission_error(self):
        tc = transmissionrpc_client()
        self.assertIsNone(tc)


class TransmissionrpcAddTorrentLogicTests(TestCase):
    def test_ok(self):
        tc = MagicMock()
        tc_add_torrent = MagicMock()
        tc.add_torrent = tc_add_torrent

        success = transmissionrpc_add_torrent(tc, 'fake_file')
        tc_add_torrent.assert_called_once()
        self.assertTrue(success)

    def test_transmission_error(self):
        tc = MagicMock()
        tc_add_torrent = raise_exception
        tc.add_torrent = tc_add_torrent

        success = transmissionrpc_add_torrent(tc, 'fake_file')
        self.assertFalse(success)
