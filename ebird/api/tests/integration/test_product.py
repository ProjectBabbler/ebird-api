# -*- coding: utf-8 -*-

from unittest import TestCase

from ebird.api import region_notable, hotspot_summary


class ProductIntegrationTest(TestCase):
    """Tests for the product-related end-points in the eBird API."""

    @classmethod
    def setUpClass(cls):
        records = region_notable('US-NY', hotspot=True)
        cls.location = records[0]['locID']

    def test_hotspot_summary(self):
        hotspot_summary(self.location)
