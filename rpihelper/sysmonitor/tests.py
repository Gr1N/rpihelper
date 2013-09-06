# -*- coding: utf-8 -*-

from unittest.mock import patch

from flask import json

from rpihelper.sysmonitor.logic import get_temperature, get_voltage
from rpihelper.test import TestCase, ViewTestCase

__all__ = (
    'IndexViewTests',
    'SystemInfoViewTests',

    'GetTemperatureLogicTests',
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
                'temperature',
                'voltage',
            ]),
            sorted(list(data.keys()))
        )


class GetTemperatureLogicTests(TestCase):
    def _test_temperature(self, vcgencmd_output):
        with patch('rpihelper.sysmonitor.logic.get_vcgencmd',
                   new=lambda *args: vcgencmd_output):
            return get_temperature()

    def test_ok(self):
        vcgencmd_output = 'temp=42\'C'
        temperature = self._test_temperature(vcgencmd_output)
        self.assertEqual(temperature, vcgencmd_output.split('=')[-1])

    def test_bad_output(self):
        temperature = self._test_temperature('/bad/output')
        self.assertIsNone(temperature)


class GetVoltageLogicTests(TestCase):
    def _test_voltage(self, vcgencmd_output):
        with patch('rpihelper.sysmonitor.logic.get_vcgencmd',
                   new=lambda *args: vcgencmd_output):
            voltage = get_voltage()
            self.assertListEqual(
                sorted(['core', 'io', 'phy',]),
                sorted(list(voltage.keys()))
            )

            return voltage

    def test_ok(self):
        vcgencmd_output = 'volt=1.20V'
        voltage = self._test_voltage(vcgencmd_output)

        for volt in voltage.values():
            self.assertEqual(volt, vcgencmd_output.split('=')[-1])

    def test_bad_output(self):
        voltage = self._test_voltage('/bad/output')

        for volt in voltage.values():
            self.assertIsNone(volt)
