# -*- coding: utf-8 -*-

import os
import sys


BASE_DIR = os.path.join(os.path.dirname(__file__))


activate_this = os.path.join(BASE_DIR, 'env/bin/activate_this.py')
execfile(activate_this, dict(__file__=activate_this))


if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)


from rpihelper import create_app
application = create_app()
