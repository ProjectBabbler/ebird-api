# -*- coding: utf-8 -*-

import os
import unittest

from setuptools import setup


def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as fp:
        return fp.read()


def test_suite():
    # Force test discovery to only look at the tests directory
    # otherwise all the tests get executed twice.
    test_loader = unittest.TestLoader()
    return test_loader.discover('tests', pattern='test_*.py')


setup(
    name='ebird-api',
    version='3.0.0',
    description='Wrapper for accessing the eBird API',
    long_description=read("README.md"),
    long_description_content_type='text/markdown',
    author='ProjectBabbler',
    author_email='projectbabbler@gmail.com',
    url='http://pypi.python.org/pypi/ebird-api/',
    license='GPL',
    keywords='eBird API client',
    packages=['ebird.api'],
    test_suite='setup.test_suite',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Natural Language :: English',
        'Topic :: Utilities',
        'Topic :: Internet',
    ],
)
