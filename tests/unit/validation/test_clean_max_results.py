import unittest

from ebird.api.requests.validation import clean_max_results


class CleanMaxResultsTests(unittest.TestCase):
    """Tests for the clean_max_results validation function."""

    def test_none_is_allowed(self):
        self.assertEqual(None, clean_max_results(None, 10000))

    def test_string_converts_to_integer(self):
        self.assertEqual(10, clean_max_results("10", 10000))

    def test_value_outside_range(self):
        self.assertRaises(ValueError, clean_max_results, 0, 10000)
        self.assertRaises(ValueError, clean_max_results, 10001, 10000)
