# -*- coding: utf-8 -*-

from flask import json

from rpihelper.test import ViewTestCase

__all__ = (
    'IndexViewTests',
    'SystemInfoViewTests',
)


class IndexViewTests(ViewTestCase):
    view_rule = 'sysmonitor.index'

    def test_get_ok(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)

    def test_post_not_allowed(self):
        response = self.client.post(self.view_url)
        self.assertEqual(response.status_code, 405)


class SystemInfoViewTests(ViewTestCase):
    view_rule = 'sysmonitor.system_info'

    def test_get_not_allowed(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 405)

    def test_post_ok(self):
        response = self.client.post(self.view_url)
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
