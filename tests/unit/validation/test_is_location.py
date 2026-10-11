import unittest

from ebird.api.requests.validation import is_location


class IsLocationTests(unittest.TestCase):
    """Tests for the is_location validation function."""

    def test_is_location(self):
        self.assertTrue(is_location("L123456"))

    def test_invalid_code_is_not_location(self):
        self.assertFalse(is_location("A123456"))

    def test_country_is_not_location(self):
        self.assertFalse(is_location("US"))

    def test_subnational1_is_not_location(self):
        self.assertFalse(is_location("US-NV"))

    def test_subnational12_is_not_location(self):
        self.assertFalse(is_location("US-NV-11"))
