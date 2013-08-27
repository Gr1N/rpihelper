# -*- coding: utf-8 -*-

from unittest import TestCase as _TestCase

from flask import template_rendered, url_for

from rpihelper import create_app

__all__ = (
    'TestCase',
    'ViewTestCase',
)


class TestCase(_TestCase):
    def setUp(self):
        self.app = create_app(testing=True)


class ContextVariableDoesNotExist(Exception):
    pass


class ViewTestCase(TestCase):
    view_rule = None

    def __call__(self, result=None):
        self.templates = []
        template_rendered.connect(self._add_template)

        super(ViewTestCase, self).__call__(result)

    def _add_template(self, app, template, context):
        if self.templates:
            self.templates = []
        self.templates.append((template, context))

    def setUp(self):
        super(ViewTestCase, self).setUp()
        self.client = self.app.test_client()

    def url_for(self, rule):
        with self.app.test_request_context():
            return url_for(rule)

    @property
    def view_url(self):
        return self.url_for(self.view_rule)

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
