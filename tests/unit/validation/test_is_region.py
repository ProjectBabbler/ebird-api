import unittest

from ebird.api.requests.validation import is_region


class IsRegionTests(unittest.TestCase):
    """Tests for the is_region validation function."""

    def test_country_is_region(self):
        self.assertTrue(is_region("US"))

    def test_single_character_subnational1_is_not_region(self):
        self.assertFalse(is_region("AR-A"))
        self.assertFalse(is_region("AR-1"))

    def test_two_character_subnational1_is_region(self):
        self.assertTrue(is_region("US-NV"))
        self.assertTrue(is_region("US-12"))

    def test_three_character_subnational1_is_region(self):
        self.assertTrue(is_region("US-NVA"))
        self.assertTrue(is_region("US-122"))

    def test_single_character_subnational2_is_not_region(self):
        self.assertFalse(is_region("US-NV-A"))
        self.assertFalse(is_region("US-NV-1"))

    def test_two_character_subnational2_is_region(self):
        self.assertTrue(is_region("US-NV-AB"))
        self.assertTrue(is_region("US-NV-11"))

    def test_location_is_not_region(self):
        self.assertFalse(is_region("L123456"))
