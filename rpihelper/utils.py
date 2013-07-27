# -*- coding: utf-8 -*-

import os

__all__ = (
    'INSTANCE_FOLDER_PATH',

    'make_dir',
)


# Instance folder path, make it independent.
INSTANCE_FOLDER_PATH = os.path.join('/tmp', 'rpihelper')


def make_dir(dir_path):
    try:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    except Exception as e:
        raise e
