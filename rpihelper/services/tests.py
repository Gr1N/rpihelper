# -*- coding: utf-8 -*-

from unittest.mock import patch, MagicMock

from flask import json

from rpihelper.services.logic import SystemctlCommands
from rpihelper.test import ViewTestCase

__all__ = (
    'IndexViewTests',
    'SendServiceCommandTests',
)


class IndexViewTests(ViewTestCase):
    view_rule = 'services.index'

    def test_get_ok(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)

        self.assertTrue(self.get_context_variable('services'))

    def test_post_not_allowed(self):
        response = self.client.post(self.view_url)
        self.assertEqual(response.status_code, 405)


class SendServiceCommandTests(ViewTestCase):
    view_rule = 'services.send_service_command'

    def patch_services(self):
        return patch('rpihelper.services.forms.get_services', return_value=(
            {
                'name': 'test1',
                'description': 'description1',
                'url': 'url1',
            },
            {
                'name': 'test2',
                'description': 'description2',
                'url': 'url2',
            }
        ))

    def test_get_not_allowed(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 405)

    def test_post_form_invalid(self):
        response = self.client.post(self.view_url)
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        errors = data['errors']
        self.assertIn('service', errors)
        self.assertIn('command', errors)

    def test_post_form_invalid_unknown_service(self):
        with self.patch_services():
            response = self.client.post(self.view_url, data={
                'command': SystemctlCommands.STOP,
                'service': 'test',
            })

            data = json.loads(response.data)
            self.assertEqual(data['status'], 'error')
            errors = data['errors']
            self.assertIn('service', errors)

    @patch('rpihelper.services.views.call_command', new=MagicMock())  # TODO: remove this patch and run tests
    def test_post_form_valid(self):
        with self.patch_services():
            response = self.client.post(self.view_url, data={
                'command': SystemctlCommands.STOP,
                'service': 'test1',
            })

            data = json.loads(response.data)
            self.assertEqual(data['status'], 'ok')
