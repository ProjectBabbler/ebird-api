# -*- coding: utf-8 -*-

"""A set of wrapper functions for accessing the eBird API."""

from ebird.api.version import __version__

# noinspection PyUnresolvedReferences
from ebird.api.data import geo_observations, geo_notable, geo_species, \
    region_observations, region_notable, region_species, \
    hotspot_observations, hotspot_notable, hotspot_species, \
    location_observations, location_notable, location_species, \
    nearest_species

from ebird.api.product import  hotspot_summary

from ebird.api.reference import  list_hotspots, nearest_hotspots, \
    find_regions, list_regions, list_species
