import unittest

from ebird.api.requests.validation import clean_back


class CleanBackTests(unittest.TestCase):
    """Tests for the clean_back validation function."""

    def test_string_converts_to_integer(self):
        self.assertEqual(10, clean_back("10"))

    def test_value_outside_range(self):
        self.assertRaises(ValueError, clean_back, 0)
        self.assertRaises(ValueError, clean_back, 31)
