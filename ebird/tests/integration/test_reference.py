# -*- coding: utf-8 -*-

from unittest import TestCase

from ebird import list_regions, find_regions, list_hotspots, \
    nearest_hotspots, list_species


# noinspection PyMethodMayBeStatic
class ReferenceIntegrationTests(TestCase):
    """Tests for the reference related end-points in the eBird API."""

    def test_list_regions(self):
        list_regions('country')

    def test_find_regions(self):
        find_regions('subnational1', match='west')

    def test_list_hotspots(self):
        list_hotspots('US-NV', back=10)

    def test_nearest_hotspots(self):
        nearest_hotspots(42.46, -71.25, back=1)

    def test_list_species(self):
        list_species()
