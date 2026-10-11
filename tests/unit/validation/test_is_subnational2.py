import unittest

from ebird.api.requests.validation import is_subnational2


class IsSubnational2Tests(unittest.TestCase):
    """Tests for the is_subnational2 validation function."""

    def test_is_subnational2(self):
        self.assertTrue(is_subnational2("US-NV-11"))

    def test_invalid_code_is_not_subnational2(self):
        self.assertFalse(is_subnational2("US-NV-"))

    def test_country_is_not_subnational2(self):
        self.assertFalse(is_subnational2("US"))

    def test_subnational1_is_not_subnational2(self):
        self.assertFalse(is_subnational2("US-NV"))

    def test_location_is_not_subnational2(self):
        self.assertFalse(is_subnational2("L123456"))
