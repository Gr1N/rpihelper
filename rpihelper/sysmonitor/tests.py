# -*- coding: utf-8 -*-

from flask import url_for

from rpihelper.test import ViewTestCase

__all__ = (
    'SysMonitorIndexViewTests',
)


class SysMonitorIndexViewTests(ViewTestCase):
    def test_get_ok(self):
        with self.app.test_request_context():
            response = self.client.get(url_for('sysmonitor.index'))
            self.assertEqual(response.status_code, 200)

            self.assertTrue(self.get_context_variable('virtual_memory'))
            self.assertTrue(self.get_context_variable('swap_memory'))
            self.assertTrue(self.get_context_variable('cpu'))

    def test_post_not_allowed(self):
        with self.app.test_request_context():
            response = self.client.post(url_for('sysmonitor.index'))
            self.assertEqual(response.status_code, 405)
