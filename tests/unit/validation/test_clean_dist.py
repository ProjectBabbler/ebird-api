import unittest

from ebird.api.requests.validation import clean_dist


class CleanDistTests(unittest.TestCase):
    """Tests for the clean_dist validation function."""

    def test_string_converted_to_integer(self):
        self.assertEqual(10, clean_dist("10"))

    def test_value_outside_range(self):
        self.assertRaises(ValueError, clean_dist, -1)
        self.assertRaises(ValueError, clean_dist, 51)
