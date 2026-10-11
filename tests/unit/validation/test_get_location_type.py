import unittest

from ebird.api.requests.validation import get_location_type


class GetLocationTypeTests(unittest.TestCase):
    """Tests for the get_region_type function."""

    def test_country(self):
        self.assertEqual("country", get_location_type("US"))

    def test_country_lower_case(self):
        self.assertIsNone(get_location_type("us"))

    def test_subnational1(self):
        self.assertEqual("subnational1", get_location_type("US-NV"))
        self.assertEqual("subnational1", get_location_type("MX-OXA"))

    def test_subnational1_lower_case(self):
        self.assertIsNone(get_location_type("us-nv"))

    def test_subnational2(self):
        self.assertEqual("subnational2", get_location_type("US-NV-11"))
        self.assertEqual("subnational2", get_location_type("US-NV-112"))

    def test_subnational2_lower_case(self):
        self.assertIsNone(get_location_type("us-nv-11"))

    def test_location(self):
        self.assertEqual("location", get_location_type("L123456"))

    def test_location_lower_case(self):
        self.assertIsNone(get_location_type("l123456"))

    def test_unknown_location_type(self):
        self.assertEqual(None, get_location_type("world"))

    def test_location_type_must_be_a_string(self):
        self.assertRaises(ValueError, get_location_type, 123)
