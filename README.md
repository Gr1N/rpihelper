Raspberry Pi Helper (RPiHelper)
===============================

**Raspberry Pi Helper** is a very lightweight system monitoring, services management (via `systemd`) tool and etc.


Features
--------

* System monitoring
* Services management (via `systemd`)
* [Transmission](http://www.transmissionbt.com/) helper - background task sync [DropBox](https://www.dropbox.com/) folder for new torrent files and add to Transmission


Development
-----------

    mkvirtualenv rpihelper --python=python3
    pip install -U -r .meta/packages
    python manage.py runserver/test


Deployment
----------

Use *fabfile.py* and *nginx*/*httpd*/*supervisor* configs from repo for deployment.


License
-------

RPiHelper is distributed under the [MIT license](http://www.opensource.org/licenses/MIT).
