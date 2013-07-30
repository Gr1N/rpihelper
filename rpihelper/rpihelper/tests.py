# -*- coding: utf-8 -*-

from flask import url_for

from rpihelper.test import ViewTestCase

__all__ = (
    'RPiHelperIndexViewTests',
)


class RPiHelperIndexViewTests(ViewTestCase):
    def test_get_ok(self):
        with self.app.test_request_context():
            response = self.client.get(url_for('rpihelper.index'))
            self.assertEqual(response.status_code, 200)

    def test_post_not_allowed(self):
        with self.app.test_request_context():
            response = self.client.post(url_for('rpihelper.index'))
            self.assertEqual(response.status_code, 405)
