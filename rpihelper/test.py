# -*- coding: utf-8 -*-

import unittest

from flask import template_rendered

from rpihelper import create_app

__all__ = (
    'ViewTestCase',
)


class ContextVariableDoesNotExist(Exception):
    pass


class ViewTestCase(unittest.TestCase):
    def __call__(self, result=None):
        self.templates = []
        template_rendered.connect(self._add_template)

        super(ViewTestCase, self).__call__(result)

    def _add_template(self, app, template, context):
        if self.templates:
            self.templates = []
        self.templates.append((template, context))

    def setUp(self):
        self.app = create_app(testing=True)
        self.client = self.app.test_client()

    def get_context_variable(self, name):
        for template, context in self.templates:
            if name in context:
                return context[name]
        raise ContextVariableDoesNotExist

    def assertContext(self, name, value):
        try:
            self.assertEqual(self.get_context_variable(name), value)
        except ContextVariableDoesNotExist:
            self.fail('Context variable does not exist: %s' % name)
