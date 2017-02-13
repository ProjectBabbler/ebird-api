# -*- coding: utf-8 -*-

from unittest import TestCase

from ebird.core import \
    geo_observations, geo_species, geo_notable, \
    hotspot_observations, hotspot_species, hotspot_notable, \
    location_observations, location_species, location_notable, \
    region_observations, region_species, region_notable, \
    nearest_species


class CoreIntegrationTests(TestCase):
    """Tests for the core functions which call the eBird API."""

    lat = 42.48
    lng = -76.45
    region = 'US-NY-061'
    hotspot = 'L227544'
    location = 'L227544'
    species = 'Branta canadensis'

    def test_geo_observations(self):
        geo_observations(self.lat, self.lng)

    def test_geo_species(self):
        geo_species(self.species, self.lat, self.lng)

    def test_geo_notable(self):
        geo_notable(self.lat, self.lng)

    def test_hotspot_observations(self):
        hotspot_observations(self.hotspot)

    def test_hotspot_species(self):
        hotspot_species(self.species, self.hotspot)

    def test_hotspot_notable(self):
        hotspot_notable(self.hotspot)

    def test_location_observations(self):
        location_observations(self.location)

    def test_location_species(self):
        location_species(self.species, self.location)

    def test_location_notable(self):
        location_notable(self.location)

    def test_region_observations(self):
        region_observations(self.region)

    def test_region_species(self):
        region_species(self.species, self.region)

    def test_region_notable(self):
        region_notable(self.region)

    def test_nearest_species(self):
        nearest_species(self.species, self.lat, self.lng)
