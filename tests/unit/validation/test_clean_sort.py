import unittest

from ebird.api.requests.validation import clean_sort


class CleanSortTests(unittest.TestCase):
    """Tests for the clean_sort validation function."""

    def test_code_is_lower_case(self):
        self.assertEqual("date", clean_sort("Date"))

    def test_invalid_code_raises_error(self):
        self.assertRaises(ValueError, clean_sort, "none")
