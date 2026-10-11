import unittest

from ebird.api.requests.validation import is_country


class IsCountryTests(unittest.TestCase):
    """Tests for the is_country validation function."""

    def test_is_country(self):
        self.assertTrue(is_country("US"))

    def test_invalid_code_is_not_country(self):
        self.assertFalse(is_country("U"))
        self.assertFalse(is_country("US-"))

    def test_subnational1_is_not_country(self):
        self.assertFalse(is_country("US-NV"))
        self.assertFalse(is_country("MX-OXA"))

    def test_subnational2_is_not_country(self):
        self.assertFalse(is_country("US-NV-VMT"))

    def test_location_is_not_country(self):
        self.assertFalse(is_country("L123456"))
