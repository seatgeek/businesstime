#!/usr/bin/env python
from businesstime import __version__

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='businesstime',
    version=__version__,
    author='SeatGeek',
    author_email='hi@seatgeek.com',
    packages=['businesstime'],
    url='http://github.com/seatgeek/businesstime',
    license=open('LICENSE.txt').read(),
    classifiers=[
        'Programming Language :: Python :: 2.7',
    ],
    description='A simple utility for calculating business time aware timedeltas between two datetimes',
    long_description=open('README.rst').read() + '\n\n' +
                     open('CHANGES.rst').read(),
    tests_require=['nose'],
    test_suite='nose.collector'
)
