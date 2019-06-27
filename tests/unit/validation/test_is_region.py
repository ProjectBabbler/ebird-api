import unittest

from ebird.api.validation import is_region


class IsRegionTests(unittest.TestCase):
    """Tests for the is_region validation function."""

    def test_country_is_region(self):
        self.assertTrue(is_region('US'))

    def test_subnational1_is_region(self):
        self.assertTrue(is_region('US-NV'))

    def test_subnational2_is_region(self):
        self.assertTrue(is_region('US-NV-11'))

    def test_location_is_not_region(self):
        self.assertFalse(is_region('L123456'))
