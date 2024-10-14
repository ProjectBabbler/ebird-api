import unittest

from ebird.api.validation import is_subnational1


class IsSubnational1Tests(unittest.TestCase):
    """Tests for the is_subnational1 validation function."""

    def test_is_subnational1(self):
        self.assertTrue(is_subnational1("US-NV"))

    def test_invalid_code_is_not_subnational1(self):
        self.assertFalse(is_subnational1("U"))
        self.assertFalse(is_subnational1("US-"))

    def test_country_is_not_subnational1(self):
        self.assertFalse(is_subnational1("US"))

    def test_subnational2_is_not_subnational1(self):
        self.assertFalse(is_subnational1("US-NV-VMT"))

    def test_location_is_not_subnational1(self):
        self.assertFalse(is_subnational1("L123456"))
