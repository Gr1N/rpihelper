# -*- coding: utf-8 -*-

from unittest.mock import patch, MagicMock

from flask import json

from rpihelper.services.logic import (
    SystemctlCommands, SystemctlStatuses,
    systemctl_ssr_command, systemctl_status_command,
)
from rpihelper.services.views import ERR_EXECUTE_COMMAND
from rpihelper.test import TestCase, ViewTestCase

__all__ = (
    'IndexViewTests',
    'SendServiceCommandViewTests',

    'SystemctlSSRCommandLogicTests',
    'SystemctlStatusCommandLogicTests',
)


SYSTEMCTL_SSR_ERROR_OUTPUT = """
Failed to issue method call: Unit tran.service not loaded.
"""
SYSTEMCTL_STATUS_INACTIVE_OUTPUT = """
transmission.service - Transmission BitTorrent Daemon
Loaded: loaded (/usr/lib/systemd/system/transmission.service; enabled)
Drop-In: /etc/systemd/system/transmission.service.d
       └─user.conf
Active: inactive (dead) since Mon 2013-08-26 21:07:36 FET; 27min ago
Process: 5290 ExecStart=/usr/bin/transmission-daemon -f --log-error (code=exited, status=0/SUCCESS)
"""
SYSTEMCTL_STATUS_ACTIVE_OUTPUT = """
transmission.service - Transmission BitTorrent Daemon
Loaded: loaded (/usr/lib/systemd/system/transmission.service; enabled)
Drop-In: /etc/systemd/system/transmission.service.d
       └─user.conf
Active: active (running) since Mon 2013-08-26 21:07:36 FET; 27min ago
Process: 5290 ExecStart=/usr/bin/transmission-daemon -f --log-error (code=exited, status=0/SUCCESS)
"""
SYSTEMCTL_STATUS_ERROR_OUTPUT = """
transmissio.service
Loaded: error (Reason: No such file or directory)
Active: inactive (dead)
"""


class IndexViewTests(ViewTestCase):
    view_rule = 'services.index'

    @patch('rpihelper.services.logic.systemctl_status_command', new=MagicMock())
    def test_get_ok(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)

        self.assertTrue(self.get_context_variable('services'))

    def test_post_not_allowed(self):
        response = self.client.post(self.view_url)
        self.assertEqual(response.status_code, 405)


class SendServiceCommandViewTests(ViewTestCase):
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

    @patch('rpihelper.services.views.systemctl_ssr_command', new=lambda *args, **kwargs: False)
    def test_post_form_valid(self):
        with self.patch_services():
            response = self.client.post(self.view_url, data={
                'command': SystemctlCommands.STOP,
                'service': 'test1',
            })

            data = json.loads(response.data)
            self.assertEqual(data['status'], 'ok')

    @patch('rpihelper.services.views.systemctl_ssr_command', new=lambda *args, **kwargs: True)
    def test_post_form_valid_error_while_executing_command(self):
        with self.patch_services():
            command = SystemctlCommands.STOP
            service = 'test1'

            response = self.client.post(self.view_url, data={
                'command': command,
                'service': service,
            })

            data = json.loads(response.data)
            self.assertEqual(data['status'], 'error')
            self.assertEqual(data['error'], ERR_EXECUTE_COMMAND % (command, service))


class SystemctlCommandLogicMixin(object):
    def patch_getoutput(self, output):
        return patch(
            'rpihelper.services.logic.getoutput',
            new=lambda *args, **kwargs: output
        )


class SystemctlSSRCommandLogicTests(TestCase, SystemctlCommandLogicMixin):
    def _test_ssr(self, output, expected_error=False):
        assertMethod = self.assertTrue if expected_error else self.assertFalse

        with self.app.test_request_context():
            with self.patch_getoutput(output):
                error = systemctl_ssr_command('command', 'service')
                assertMethod(error)

    def test_no_error(self):
        self._test_ssr('')

    def test_error(self):
        self._test_ssr(SYSTEMCTL_SSR_ERROR_OUTPUT, expected_error=True)


class SystemctlStatusCommandLogicTests(TestCase, SystemctlCommandLogicMixin):
    def _test_status(self, output, expected_status):
        with self.app.test_request_context():
            with self.patch_getoutput(output):
                status = systemctl_status_command('service')
                self.assertEqual(status, expected_status)

    def test_status_active(self):
        self._test_status(SYSTEMCTL_STATUS_ACTIVE_OUTPUT, SystemctlStatuses.ACTIVE)

    def test_status_inactive(self):
        self._test_status(SYSTEMCTL_STATUS_INACTIVE_OUTPUT, SystemctlStatuses.INACTIVE)

    def test_status_error(self):
        self._test_status(SYSTEMCTL_STATUS_ERROR_OUTPUT, SystemctlStatuses.INACTIVE)

    def test_no_output(self):
        self._test_status('', SystemctlStatuses.UNKNOWN)

