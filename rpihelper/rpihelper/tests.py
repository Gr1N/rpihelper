# -*- coding: utf-8 -*-

from rpihelper.test import ViewTestCase

__all__ = (
    'IndexViewTests',
)


class IndexViewTests(ViewTestCase):
    view_rule = 'rpihelper.index'

    def test_get_ok(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)

    def test_post_not_allowed(self):
        response = self.client.post(self.view_url)
        self.assertEqual(response.status_code, 405)
