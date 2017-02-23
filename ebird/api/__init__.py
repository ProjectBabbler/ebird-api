# -*- coding: utf-8 -*-

"""A set of wrapper functions for accessing the eBird API."""

# noinspection PyUnresolvedReferences
from ebird.api.data import geo_observations, geo_notable, geo_species, \
    region_observations, region_notable, region_species, \
    hotspot_observations, hotspot_notable, hotspot_species, \
    location_observations, location_notable, location_species, \
    nearest_species

from ebird.api.product import  hotspot_summary

from ebird.api.reference import  list_hotspots, nearest_hotspots, \
    find_regions, list_regions, list_species


VERSION = (2, 0, 0, 'final')


def get_version():
    main = '.'.join(str(x) for x in VERSION[:3])
    sub = '-' + VERSION[3] if VERSION[3] != 'final' else ''
    return str(main + sub)
