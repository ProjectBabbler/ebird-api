import unittest

from ebird.api.requests.validation import clean_lat


class CleanLatTests(unittest.TestCase):
    """Tests for the clean_lat validation function."""

    def test_float_converts_to_string(self):
        self.assertEqual("45.34", clean_lat(45.34))

    def test_value_outside_range(self):
        self.assertRaises(ValueError, clean_lat, -90.01)
        self.assertRaises(ValueError, clean_lat, 90.01)

    def test_precision_is_limited(self):
        self.assertEqual("74.34", clean_lat(74.336))
