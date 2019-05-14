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
    version='2.1.1',
    description='Wrapper for accessing the eBird API',
    long_description=read("README.md"),
    long_description_content_type='text/markdown',
    author='ProjectBabbler',
    author_email='projectbabbler@gmail.com',
    url='http://pypi.python.org/pypi/ebird-api/',
    license='GPL',
    keywords='eBird API client',
    packages=['ebird.api'],
    entry_points="""
        [console_scripts]
        find-regions=ebird.api.scripts.find_regions:cli
        list-regions=ebird.api.scripts.list_regions:cli
        list-hotspots=ebird.api.scripts.list_hotspots:cli
        list-species=ebird.api.scripts.list_species:cli        
        nearest-hotspots=ebird.api.scripts.nearest_hotspots:cli        
        nearest-species=ebird.api.scripts.nearest_species:cli        
        geo-observations=ebird.api.scripts.geo_observations:cli        
        geo-notable=ebird.api.scripts.geo_notable:cli        
        geo-species=ebird.api.scripts.geo_species:cli        
        hotspot-observations=ebird.api.scripts.hotspot_observations:cli        
        hotspot-notable=ebird.api.scripts.hotspot_notable:cli        
        hotspot-species=ebird.api.scripts.hotspot_species:cli        
        hotspot-summary=ebird.api.scripts.hotspot_summary:cli        
        location-observations=ebird.api.scripts.location_observations:cli        
        location-notable=ebird.api.scripts.location_notable:cli        
        location-species=ebird.api.scripts.location_species:cli        
        region-observations=ebird.api.scripts.region_observations:cli        
        region-notable=ebird.api.scripts.region_notable:cli        
        region-species=ebird.api.scripts.region_species:cli        
    """,
    test_suite='setup.test_suite',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Natural Language :: English',
        'Topic :: Utilities',
        'Topic :: Internet',
    ],
    install_requires=[
        'Click'
    ],
)
