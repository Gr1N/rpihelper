# -*- coding: utf-8 -*-

from distutils.core import setup
from setuptools import find_packages


with open('.meta/packages') as reqs:
    install_requires = reqs.read().split('\n')


setup(
    name='rpihelper',
    version='0.0.2',
    author='Nikita Grishko',
    author_email='grin.minsk@gmail.com',
    url='https://github.com/Gr1N/rpihelper',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
