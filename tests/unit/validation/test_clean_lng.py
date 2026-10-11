import unittest

from ebird.api.requests.validation import clean_lng


class CleanLngTests(unittest.TestCase):
    """Tests for the clean_lng validation function."""

    def test_float_converted_to_string(self):
        self.assertEqual("45.34", clean_lng(45.34))

    def test_value_outside_range(self):
        self.assertRaises(ValueError, clean_lng, -180.01)
        self.assertRaises(ValueError, clean_lng, 180.01)

    def test_precision_is_limited(self):
        self.assertEqual("74.34", clean_lng(74.344))
