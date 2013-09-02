# -*- coding: utf-8 -*-

from rpihelper.dropboxclient.logic import Client
from rpihelper.test import TestCase

__all__ = (
    'DropBoxClientLogicTests',
)


DROPBOX_TEST_FOLDER = '/Public/'


class DropBoxClientLogicTests(TestCase):
    """
    Testing DropBox client.

    Note: all tests requires valid settings (`DROPBOX_`)
    and you should be connected to internet.
    """

    def setUp(self):
        super(DropBoxClientLogicTests, self).setUp()

        with self.app.test_request_context():
            self.client = Client()

    def test_folder(self):
        files = self.client.folder(DROPBOX_TEST_FOLDER)
        self.assertTrue(isinstance(files, list))

    def test_file(self):
        file_name = self.client.folder(DROPBOX_TEST_FOLDER)[0]
        file = self.client.file(file_name)
        self.assertTrue(isinstance(file, bytes))

    def test_file_url(self):
        file_name = self.client.folder(DROPBOX_TEST_FOLDER)[0]
        file_url = self.client.file_url(file_name)
        self.assertTrue(isinstance(file_url, str))
        self.assertTrue(file_url.startswith('http'))
