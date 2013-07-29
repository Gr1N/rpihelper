# -*- coding: utf-8 -*-

import unittest

from rpihelper import create_app

__all__ = (
    'TestCase',
)


class TestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(testing=True)
        self.client = self.app.test_client()
