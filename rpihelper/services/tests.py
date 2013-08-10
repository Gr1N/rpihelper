# -*- coding: utf-8 -*-

from flask import url_for

from rpihelper.test import ViewTestCase

__all__ = (
    'ServicesIndexViewTests',
)


class ServicesIndexViewTests(ViewTestCase):
    def test_get_ok(self):
        with self.app.test_request_context():
            response = self.client.get(url_for('services.index'))
            self.assertEqual(response.status_code, 200)

            self.assertTrue(self.get_context_variable('services'))

    def test_post_not_allowed(self):
        with self.app.test_request_context():
            response = self.client.post(url_for('services.index'))
            self.assertEqual(response.status_code, 405)
