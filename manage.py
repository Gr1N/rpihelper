# -*- coding: utf-8 -*-

import os

from flask.ext.script import Manager

from rpihelper import create_app


app = create_app()
manager = Manager(app)


@manager.command
@manager.option('-tm', '--testmodule', help='Provide test module')
def test(testmodule='discover'):
    """Run unit tests."""
    os.environ['FLASK_ENV'] = 'testing'
    os.system('python -m unittest %s' % testmodule)


if __name__ == '__main__':
    manager.run()
