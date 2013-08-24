# -*- coding: utf-8 -*-

from flask import url_for, json

from rpihelper.test import ViewTestCase

__all__ = (
    'IndexViewTests',
    'SystemInfoViewTests',
)


class IndexViewTests(ViewTestCase):
    def test_get_ok(self):
        with self.app.test_request_context():
            response = self.client.get(url_for('sysmonitor.index'))
            self.assertEqual(response.status_code, 200)

    def test_post_not_allowed(self):
        with self.app.test_request_context():
            response = self.client.post(url_for('sysmonitor.index'))
            self.assertEqual(response.status_code, 405)


class SystemInfoViewTests(ViewTestCase):
    def test_post_ok(self):
        with self.app.test_request_context():
            response = self.client.post(url_for('sysmonitor.system_info'))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')

            data = json.loads(response.data)
            self.assertEqual(data['status'], 'ok')

            data = data['data']
            self.assertListEqual(
                sorted([
                    'boot_time',
                    'virtual_memory',
                    'swap_memory',
                    'cpu',
                    'disks',
                    'processes',
                ]),
                sorted(list(data.keys()))
            )
