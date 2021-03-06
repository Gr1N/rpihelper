# -*- coding: utf-8 -*-

import os

import yaml

from flask import Flask as BaseFlask, Config as BaseConfig

__all__ = (
    'Flask',
)


class Config(BaseConfig):
    """
    Flask config enhanced with a `from_yaml` method.
    """

    def __init__(self, *args, **kwargs):
        super(Config, self).__init__(*args, **kwargs)

        self['PROJECT_ROOT'] = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    def from_yaml(self, config_file):
        env = os.environ.get('FLASK_ENV', 'development').upper()
        self['ENVIRONMENT'] = env.lower()

        with open(config_file) as f:
            c = yaml.load(f)

        c = c.get(env, c)

        for key in c.keys():
            if key.isupper():
                self[key] = c[key]


class Flask(BaseFlask):
    """
    Extended version of `Flask` that implements custom config class.
    """

    def make_config(self, instance_relative=False):
        root_path = self.root_path
        if instance_relative:
            root_path = self.instance_path
        return Config(root_path, self.default_config)
